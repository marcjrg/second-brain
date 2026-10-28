"""Independent, fail-closed Codex app-server watchdog using Python stdlib only.

IMPORTANT: This launcher supervises ONLY workers it launches, not an already running
Codex desktop/Work session. It never approves a server-initiated request.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from typing import Any

TERMINAL = {"COMPLETE", "BLOCKED", "SKIPPED"}
ACTIVE = {"RUNNING", "INTERRUPTING", "DIAGNOSING", "RECOVERING", "WAITING_APPROVAL", "UNKNOWN"}
MAX_SPECIALISTS = 3
MAX_MESSAGE = 2_000_000


class WatchdogError(RuntimeError):
    pass


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-", text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(value, f, indent=2, sort_keys=True)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def _inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def load_plan(path: Path) -> dict:
    doc = json.loads(path.read_text(encoding="utf-8"))
    root = Path(doc["project_root"]).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise WatchdogError("project_root must be a directory")
    if len(doc.get("tasks", [])) == 0:
        raise WatchdogError("plan must contain tasks")
    if len(doc["tasks"]) > 100:
        raise WatchdogError("plan exceeds 100 tasks")
    ids, cwds = set(), set()
    for t in doc["tasks"]:
        ident = t.get("id")
        if not isinstance(ident, str) or not ident or len(ident) > 100 or ident in ids:
            raise WatchdogError("task ids must be distinct non-empty strings of at most 100 chars")
        ids.add(ident)
        if not isinstance(t.get("prompt"), str) or not t["prompt"].strip():
            raise WatchdogError(f"{ident}: nonempty prompt required")
        cwd = Path(t["cwd"]).expanduser().resolve(strict=True)
        if not cwd.is_dir() or not _inside(cwd, root):
            raise WatchdogError(f"{ident}: cwd must be an existing directory under project_root")
        if any(_inside(cwd, existing) or _inside(existing, cwd) for existing in cwds):
            raise WatchdogError("workers may not share or nest cwd paths; use isolated Git worktrees")
        cwds.add(cwd)
        t["cwd"] = str(cwd)
        for field in ("timeout_seconds", "progress_timeout_seconds"):
            value = t.get(field, 600 if field == "timeout_seconds" else 300)
            if not isinstance(value, (float, int)) or isinstance(value, bool) or not 0.1 <= value <= 86400:
                raise WatchdogError(f"{ident}: {field} must be 0.1..86400 seconds")
            t[field] = float(value)
        if not isinstance(t.get("deps", []), list) or not all(isinstance(d, str) for d in t.get("deps", [])):
            raise WatchdogError(f"{ident}: deps must be a list of task IDs")
        for rel in t.get("evidence_files", []):
            if not isinstance(rel, str):
                raise WatchdogError(f"{ident}: evidence_files entries must be paths")
            full = (cwd / rel).resolve(strict=False)
            if not _inside(full, cwd) or full == cwd:
                raise WatchdogError(f"{ident}: evidence must remain inside worker cwd")
        argv = t.get("verify_argv", [])
        if argv and (not isinstance(argv, list) or not all(isinstance(x, str) and x for x in argv)):
            raise WatchdogError(f"{ident}: verify_argv must be nonempty string argv elements")
        if not t.get("evidence_files") and not argv:
            raise WatchdogError(f"{ident}: require evidence_files and/or verify_argv for completion")
    for t in doc["tasks"]:
        if t["id"] in t.get("deps", []) or any(d not in ids for d in t.get("deps", [])):
            raise WatchdogError(f"{t['id']}: unknown or self dependency")
    graph = {t["id"]: t.get("deps", []) for t in doc["tasks"]}
    seen, visiting = set(), set()
    def visit(n: str) -> None:
        if n in visiting:
            raise WatchdogError("dependency cycle")
        if n in seen:
            return
        visiting.add(n)
        for d in graph[n]:
            visit(d)
        visiting.remove(n)
        seen.add(n)
    for n in graph:
        visit(n)
    doc["project_root"] = str(root)
    return doc


def file_fingerprint(path: Path, allowed_root: Path | None = None) -> str | None:
    if allowed_root is not None and not _inside(path.resolve(strict=False), allowed_root):
        return None
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


class ProjectLock:
    """Exclusive file lock: prevents multiple controllers using the same state dir."""
    def __init__(self, path: Path):
        self.path, self.f = path, None
    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.f = self.path.open("a+b")
        self.f.seek(0)
        if os.name == "nt":
            import msvcrt
            self.f.write(b"0")
            self.f.flush()
            self.f.seek(0)
            try:
                msvcrt.locking(self.f.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                self.f.close()
                raise WatchdogError("state dir is locked by another controller") from exc
        else:
            import fcntl
            try:
                fcntl.flock(self.f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                self.f.close()
                raise WatchdogError("state dir is locked by another controller") from exc
        return self
    def __exit__(self, *exc):
        if self.f:
            self.f.close()


class RpcClient:
    def __init__(self, command: list[str], cwd: Path):
        self.command, self.cwd = command, cwd
        self.proc: asyncio.subprocess.Process | None = None
        self.reader_task: asyncio.Task | None = None
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=512)
        self.pending: dict[int, asyncio.Future] = {}
        self.req_id = 0
        self.denied = False
        self.dead = False
        self.denied_methods: list[str] = []

    async def start(self):
        kw = {"start_new_session": True} if os.name != "nt" else {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
        self.proc = await asyncio.create_subprocess_exec(*self.command, cwd=str(self.cwd),
            stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL, **kw)
        self.reader_task = asyncio.create_task(self._read())
        await self.call("initialize", {"clientInfo": {"name": "second_brain_watchdog", "title": "Second Brain Watchdog", "version": "0.1.0"}}, timeout=10)
        await self.notify("initialized", {})

    async def _send(self, msg: dict):
        if self.proc is None or self.proc.stdin is None or self.proc.returncode is not None:
            raise WatchdogError("app-server process unavailable")
        self.proc.stdin.write((json.dumps(msg, separators=(",", ":")) + "\n").encode("utf-8"))
        await asyncio.wait_for(self.proc.stdin.drain(), timeout=5)

    async def notify(self, method: str, params: dict):
        await self._send({"method": method, "params": params})

    async def call(self, method: str, params: dict, timeout: float = 10):
        self.req_id += 1
        ident = self.req_id
        future = asyncio.get_running_loop().create_future()
        self.pending[ident] = future
        try:
            await self._send({"id": ident, "method": method, "params": params})
            return await asyncio.wait_for(future, timeout)
        finally:
            self.pending.pop(ident, None)

    async def _read(self):
        assert self.proc and self.proc.stdout
        try:
            while True:
                line = await self.proc.stdout.readline()
                if not line:
                    break
                if len(line) > MAX_MESSAGE:
                    raise WatchdogError("oversized app-server event")
                msg = json.loads(line)
                if "id" in msg and "method" not in msg:
                    future = self.pending.get(msg["id"])
                    if future and not future.done():
                        if "error" in msg:
                            future.set_exception(WatchdogError(str(msg["error"])[:500]))
                        else:
                            future.set_result(msg.get("result", {}))
                elif "id" in msg and "method" in msg:
                    # Fail closed: never approve commands, permissions, app or external actions.
                    # Responding with denial avoids an indefinitely waiting approval prompt.
                    self.denied = True
                    method = str(msg["method"])
                    self.denied_methods.append(method[:100])
                    if method in ("item/commandExecution/requestApproval", "item/fileChange/requestApproval", "execCommandApproval", "applyPatchApproval"):
                        response = {"decision": "decline"}
                    elif method == "item/permissions/requestApproval":
                        response = {"permissions": {}, "scope": "turn"}
                    elif method == "mcpServer/elicitation/request":
                        response = {"action": "decline", "content": None}
                    else:
                        # Unknown input/approvals: JSON-RPC error instead of guessed approval shape.
                        await self._send({"id": msg["id"], "error": {"code": -32601, "message": "User approval unavailable"}})
                        continue
                    await self._send({"id": msg["id"], "result": response})
                    await self._queue({"method": "watchdog/approvalDenied", "params": {"name": method}})
                elif "method" in msg:
                    await self._queue(msg)
        except (Exception, asyncio.CancelledError) as exc:
            if not isinstance(exc, asyncio.CancelledError):
                await self._queue({"method": "watchdog/transportError", "params": {"kind": type(exc).__name__}})
        finally:
            self.dead = True
            for future in self.pending.values():
                if not future.done():
                    future.set_exception(WatchdogError("app-server disconnected"))
            await self._queue({"method": "watchdog/disconnected", "params": {}})

    async def _queue(self, event: dict):
        try:
            self.queue.put_nowait(event)
        except asyncio.QueueFull:
            # No silent event loss: force the controller to fail closed.
            self.dead = True
            if self.proc and self.proc.returncode is None:
                asyncio.create_task(self.stop())

    async def interrupt(self, thread_id: str, turn_id: str):
        return await self.call("turn/interrupt", {"threadId": thread_id, "turnId": turn_id}, timeout=3)

    async def stop(self):
        proc = self.proc
        if not proc:
            return
        if proc.returncode is None:
            try:
                if os.name != "nt":
                    os.killpg(proc.pid, signal.SIGTERM)
                else:
                    proc.terminate()
                await asyncio.wait_for(proc.wait(), 1)
            except (ProcessLookupError, asyncio.TimeoutError):
                if proc.returncode is None:
                    if os.name != "nt":
                        try: os.killpg(proc.pid, signal.SIGKILL)
                        except ProcessLookupError: pass
                    else:
                        proc.kill()
                    await proc.wait()
        if self.reader_task:
            self.reader_task.cancel()
            await asyncio.gather(self.reader_task, return_exceptions=True)


@dataclass
class WorkerOutcome:
    status: str
    reason: str
    thread_id: str | None = None
    turn_id: str | None = None


class Watchdog:
    def __init__(self, doc: dict, state_dir: Path, command: list[str], allow_writes=False, allow_verify_exec=False):
        self.doc, self.state_dir, self.command = doc, state_dir, command
        self.allow_writes, self.allow_verify_exec = allow_writes, allow_verify_exec
        self.state_file = state_dir / "state.json"
        self.tasks = {t["id"]: t for t in doc["tasks"]}
        self.record = {"format": 1, "created_at": time.time(), "tasks": {
            ident: {"status": "QUEUED", "reason": "", "thread_id": None, "turn_id": None, "events": 0, "recovery_attempts": 0}
            for ident in self.tasks}}
        self.sem = asyncio.Semaphore(MAX_SPECIALISTS)
        self.active = 0
        self.peak_active = 0

    def save(self):
        self.record["updated_at"] = time.time()
        atomic_json(self.state_file, self.record)

    def update(self, ident, status, reason="", **changes):
        row = self.record["tasks"][ident]
        row.update({"status": status, "reason": reason, **changes})
        self.save()

    async def run(self):
        # On crash/uncertain previous state: NEVER reuse leases or assume a worker is gone.
        # Manual recovery requires inspecting workers and choosing a new state directory.
        if self.state_file.exists():
            raise WatchdogError(f"state exists: {self.state_file}. Inspect prior workers and use a new state directory; no automatic resume")
        self.save()
        pending = set(self.tasks)
        running: dict[str, asyncio.Task] = {}
        while pending or running:
            for ident in list(pending):
                deps = self.tasks[ident].get("deps", [])
                if any(self.record["tasks"][d]["status"] in {"BLOCKED", "SKIPPED"} for d in deps):
                    self.update(ident, "SKIPPED", "Blocked dependency")
                    pending.remove(ident)
                elif all(self.record["tasks"][d]["status"] == "COMPLETE" for d in deps):
                    if len(running) < MAX_SPECIALISTS:
                        running[ident] = asyncio.create_task(self._execute(ident))
                        pending.remove(ident)
            if not running:
                if pending:
                    raise WatchdogError("dependency scheduler deadlock")
                break
            finished, _ = await asyncio.wait(running.values(), return_when=asyncio.FIRST_COMPLETED)
            for task in finished:
                ident = next(k for k,v in running.items() if v is task)
                del running[ident]
                try:
                    outcome = task.result()
                    self.update(ident, outcome.status, outcome.reason, thread_id=outcome.thread_id, turn_id=outcome.turn_id)
                except Exception as exc:
                    self.update(ident, "BLOCKED", "Worker controller error: " + type(exc).__name__)
        return self.record

    async def _execute(self, ident: str):
        t = self.tasks[ident]
        async with self.sem:
            self.active += 1
            self.peak_active = max(self.peak_active, self.active)
            client = RpcClient(self.command, Path(t["cwd"]))
            thread_id = turn_id = None
            self.update(ident, "RUNNING", "", pid=None)
            try:
                cwd = Path(t["cwd"])
                evidence = [(cwd / r).resolve() for r in t.get("evidence_files", [])]
                before = {str(p): file_fingerprint(p, cwd) for p in evidence}
                original_before = before.copy()
                await client.start()
                self.update(ident, "RUNNING", "", pid=client.proc.pid if client.proc else None)
                params = {"cwd": str(cwd), "approvalPolicy": "onRequest", "sandbox": "workspaceWrite" if self.allow_writes else "readOnly"}
                result = await client.call("thread/start", params)
                thread_id = result["thread"]["id"]
                sandbox = {"type": "workspaceWrite", "writableRoots": [str(cwd)], "networkAccess": False} if self.allow_writes else {"type": "readOnly"}
                result = await client.call("turn/start", {"threadId": thread_id,
                    "input": [{"type": "text", "text": t["prompt"]}], "cwd": str(cwd),
                    "approvalPolicy": "onRequest", "sandboxPolicy": sandbox})
                turn_id = result["turn"]["id"]
                self.update(ident, "RUNNING", "", thread_id=thread_id, turn_id=turn_id)
                started = last_progress = time.monotonic()
                actions = no_progress = 0
                error_signatures: dict[str, int] = {}
                action_seen = set()
                reason = None
                completed = None
                while True:
                    now = time.monotonic()
                    if now-started > t["timeout_seconds"]:
                        reason = "Time budget exhausted"; break
                    if now-last_progress > t["progress_timeout_seconds"]:
                        reason = "No verified progress within budget"; break
                    if client.denied:
                        reason = "Human authorization required (request denied by headless controller)"; break
                    if client.dead and client.queue.empty():
                        reason = "App-server disconnected"; break
                    try:
                        event = await asyncio.wait_for(client.queue.get(), timeout=0.05)
                    except asyncio.TimeoutError:
                        continue
                    method, p = event.get("method"), event.get("params", {})
                    if method == "turn/completed" and p.get("turn", {}).get("id") == turn_id:
                        completed = p["turn"].get("status")
                        break
                    if method in ("watchdog/disconnected", "watchdog/transportError", "watchdog/approvalDenied"):
                        reason = "Human authorization required (denied)" if method == "watchdog/approvalDenied" else method
                        break
                    if method == "item/completed" and p.get("turnId", turn_id) == turn_id:
                        item = p.get("item") or {}
                        if item.get("type") in ("commandExecution", "fileChange", "mcpToolCall", "dynamicToolCall", "collabToolCall"):
                            key = item.get("id")
                            if key and key in action_seen:
                                continue
                            if key: action_seen.add(key)
                            actions += 1
                            cur = {str(q): file_fingerprint(q, cwd) for q in evidence}
                            advanced = bool(evidence) and cur != before and any(x is not None for x in cur.values())
                            if advanced:
                                before = cur
                                last_progress = time.monotonic()
                                no_progress = 0
                            else:
                                no_progress += 1
                            status = item.get("status")
                            if status in ("failed", "declined") or (item.get("type") == "commandExecution" and item.get("exitCode") not in (None, 0)):
                                canonical = json.dumps({"type":item.get("type"),"cmd":item.get("command"),"cwd":item.get("cwd"),"status":status,"exitCode":item.get("exitCode")},sort_keys=True,default=str)
                                sig = hashlib.sha256(canonical.encode()).hexdigest()
                                error_signatures[sig] = error_signatures.get(sig,0)+1
                                if error_signatures[sig] >= 2:
                                    reason = "Repeated equivalent failure twice"; break
                            if no_progress >= 3 or actions % 5 == 0:
                                self.update(ident, "DIAGNOSING", f"Checkpoint: {actions} actions, {no_progress} without artifact progress", events=actions)
                                self.update(ident, "RUNNING", "", events=actions)
                if reason:
                    self.update(ident, "INTERRUPTING", reason, events=actions)
                    # Interruption is not proof of cancellation. Terminate owned app-server after bounded grace.
                    try:
                        await client.interrupt(thread_id, turn_id)
                        try:
                            while True:
                                msg = await asyncio.wait_for(client.queue.get(), timeout=1)
                                if msg.get("method") == "turn/completed" and msg.get("params", {}).get("turn", {}).get("id") == turn_id:
                                    break
                        except asyncio.TimeoutError:
                            pass
                    except Exception:
                        pass
                    return WorkerOutcome("BLOCKED", reason, thread_id, turn_id)
                if completed != "completed":
                    return WorkerOutcome("BLOCKED", f"Turn ended with status {completed}", thread_id, turn_id)
                if client.denied:
                    return WorkerOutcome("BLOCKED", "Human authorization required", thread_id, turn_id)
                # Acceptance gate after turn. A model saying "done" never suffices.
                after = {str(q): file_fingerprint(q, cwd) for q in evidence}
                if evidence and any(v is None for v in after.values()):
                    return WorkerOutcome("BLOCKED", "Evidence files unavailable", thread_id, turn_id)
                if evidence and after == original_before:
                    return WorkerOutcome("BLOCKED", "Evidence unchanged since task started", thread_id, turn_id)
                if t.get("verify_argv"):
                    if not self.allow_verify_exec:
                        return WorkerOutcome("BLOCKED", "Verification command not authorized; use --allow-verify-exec", thread_id, turn_id)
                    try:
                        proc = await asyncio.create_subprocess_exec(*t["verify_argv"], cwd=str(cwd),
                            stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
                        await asyncio.wait_for(proc.wait(), timeout=min(120, t["timeout_seconds"]))
                        if proc.returncode != 0:
                            return WorkerOutcome("BLOCKED", "Verification command failed", thread_id, turn_id)
                    except asyncio.TimeoutError:
                        proc.kill()
                        await proc.wait()
                        return WorkerOutcome("BLOCKED", "Verification command timed out", thread_id, turn_id)
                if not evidence and not t.get("verify_argv"):
                    return WorkerOutcome("BLOCKED", "No verification evidence", thread_id, turn_id)
                return WorkerOutcome("COMPLETE", "Verified evidence", thread_id, turn_id)
            except Exception as exc:
                return WorkerOutcome("BLOCKED", f"Controller error: {type(exc).__name__}", thread_id, turn_id)
            finally:
                await client.stop()
                self.active -= 1


def main(argv=None) -> int:
    import argparse
    import shlex
    p = argparse.ArgumentParser(description="Opt-in Level 2 Codex app-server watchdog")
    commands = p.add_subparsers(dest="action", required=True)
    run = commands.add_parser("run", help="Run new supervised project plan")
    run.add_argument("--plan", type=Path, required=True)
    run.add_argument("--state-dir", type=Path, required=True)
    run.add_argument("--server-cmd", default="codex -c agents.enabled=false app-server", help="Command as shell-style argv (no shell used); by default disable nested Codex agents")
    run.add_argument("--allow-writes", action="store_true", help="Explicitly permit workspace writes in each task cwd")
    run.add_argument("--allow-verify-exec", action="store_true", help="Permit user-specified verification commands on host")
    stat = commands.add_parser("status", help="Display persisted state without starting workers")
    stat.add_argument("--state-dir", type=Path, required=True)
    args = p.parse_args(argv)
    if args.action == "status":
        f = args.state_dir / "state.json"
        if not f.exists():
            print("No state file", file=sys.stderr)
            return 2
        print(f.read_text(encoding="utf-8"))
        return 0
    try:
        doc = load_plan(args.plan)
        cmd = shlex.split(args.server_cmd)
        if not cmd:
            raise WatchdogError("server command empty")
        # A project-wide lock defeats attempts to bypass the cap with another state dir
        # on this same machine/account. It does not coordinate across hosts.
        project_key = hashlib.sha256(doc["project_root"].encode()).hexdigest()
        global_lock = Path.home() / ".cache" / "second-brain-watchdog" / "locks" / (project_key + ".lock")
        with ProjectLock(global_lock), ProjectLock(args.state_dir / ".watchdog.lock"):
            controller = Watchdog(doc, args.state_dir, cmd, args.allow_writes, args.allow_verify_exec)
            report = asyncio.run(controller.run())
        print(json.dumps({"tasks": report["tasks"], "peak_active": controller.peak_active}, indent=2))
        return 0 if all(row["status"] == "COMPLETE" for row in report["tasks"].values()) else 1
    except (WatchdogError, OSError, ValueError, KeyError) as exc:
        print(f"Watchdog refused execution: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
