import asyncio
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from watchdog.runtime import Watchdog, ProjectLock, WatchdogError, load_plan, main

SERVER = Path(__file__).parent / 'fake_app_server.py'

class WatchdogTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name)
        (self.base/'a').mkdir()
        self.state=self.base/'state'
        self.planfile=self.base/'plan.json'
        self.cmd=[sys.executable,str(SERVER)]

    def plan(self, scenario=None, tasks=None):
        arr = tasks if tasks is not None else [dict(id='a',cwd=str(self.base/'a'),prompt='Do a bounded task',evidence_files=['evidence.out'], timeout_seconds=3, progress_timeout_seconds=1)]
        self.planfile.write_text(json.dumps({'project_root':str(self.base),'tasks':arr}))
        return load_plan(self.planfile)

    def execute(self, scenario, tasks=None):
        plan=self.plan(tasks=tasks)
        w=Watchdog(plan,self.state,self.cmd, allow_writes=True)
        with patch.dict(os.environ,WD_SCENARIO=scenario):
            result=asyncio.run(w.run())
        return result,w

    def test_success_with_evidence(self):
        r,w=self.execute('success')
        self.assertEqual(r['tasks']['a']['status'],'COMPLETE')
        self.assertEqual(w.peak_active,1)

    def test_no_evidence_does_not_pass(self):
        r,_=self.execute('noevidence')
        self.assertEqual(r['tasks']['a']['status'],'BLOCKED')

    def test_failed_turn(self):
        r,_=self.execute('failed')
        self.assertEqual(r['tasks']['a']['status'],'BLOCKED')

    def test_approval_never_auto_accepted(self):
        r,_=self.execute('approval')
        self.assertEqual(r['tasks']['a']['status'],'BLOCKED')
        self.assertIn('authorization',r['tasks']['a']['reason'].lower())

    def test_hung_turn_interrupted(self):
        r,_=self.execute('hang')
        self.assertEqual(r['tasks']['a']['status'],'BLOCKED')
        self.assertIn('progress',r['tasks']['a']['reason'].lower())

    def test_two_equivalent_failures_halts(self):
        r,_=self.execute('twofail')
        self.assertIn('equivalent',r['tasks']['a']['reason'].lower())

    def test_independent_workers_continue_blocked_dependents(self):
        for x in ['b','c']:(self.base/x).mkdir()
        t=[dict(id='a',cwd=str(self.base/'a'),prompt='A',evidence_files=['evidence.out'],timeout_seconds=2,progress_timeout_seconds=.7),
           dict(id='b',cwd=str(self.base/'b'),prompt='B',deps=['a'],evidence_files=['evidence.out'],timeout_seconds=2,progress_timeout_seconds=.7),
           dict(id='c',cwd=str(self.base/'c'),prompt='C',evidence_files=['evidence.out'],timeout_seconds=2,progress_timeout_seconds=.7)]
        # Scenario is shared; separately fake a failure for worker a using test-specific environment extension.
        # Since all fail here, verify b skips and c has independent attempt (blocked not skipped).
        r,w=self.execute('failed',t)
        self.assertEqual(r['tasks']['a']['status'],'BLOCKED')
        self.assertEqual(r['tasks']['b']['status'],'SKIPPED')
        self.assertEqual(r['tasks']['c']['status'],'BLOCKED')

    def test_at_most_three(self):
        tasks=[]
        for n in range(6):
            q=self.base/str(n);q.mkdir()
            tasks.append(dict(id=str(n),cwd=str(q),prompt='Test',evidence_files=['evidence.out'],timeout_seconds=2,progress_timeout_seconds=.5))
        r,w=self.execute('hang',tasks)
        self.assertLessEqual(w.peak_active,3)
        self.assertGreaterEqual(w.peak_active,2)

    def test_resume_fails_closed(self):
        w=Watchdog(self.plan(),self.state,self.cmd)
        self.state.mkdir()
        (self.state/'state.json').write_text('{}')
        with self.assertRaises(WatchdogError):asyncio.run(w.run())

    def test_validation_rejects_dependency_cycles(self):
        (self.base/'b').mkdir()
        with self.assertRaises(WatchdogError):
            self.plan(tasks=[dict(id='a',cwd=str(self.base/'a'),prompt='x',deps=['b'],evidence_files=['z']),dict(id='b',cwd=str(self.base/'b'),prompt='x',deps=['a'],evidence_files=['z'])])

    def test_validation_rejects_same_cwd(self):
        with self.assertRaises(WatchdogError):
            self.plan(tasks=[dict(id='a',cwd=str(self.base/'a'),prompt='x',evidence_files=['z']),dict(id='b',cwd=str(self.base/'a'),prompt='x',evidence_files=['z'])])

    def test_validation_rejects_evidence_escape(self):
        with self.assertRaises(WatchdogError):
            self.plan(tasks=[dict(id='a',cwd=str(self.base/'a'),prompt='x',evidence_files=['../secret'])])

    def test_state_lock_exclusive(self):
        with ProjectLock(self.state/'lock'):
            with self.assertRaises(WatchdogError):
                with ProjectLock(self.state/'lock'):
                    pass

if __name__=='__main__': unittest.main()

class AdditionalValidationTests(unittest.TestCase):
    def test_nested_cwd_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t); (root/'a'/'b').mkdir(parents=True)
            p=root/'p.json';p.write_text(json.dumps({'project_root':str(root),'tasks':[
                {'id':'a','cwd':str(root/'a'),'prompt':'x','evidence_files':['x']},
                {'id':'b','cwd':str(root/'a'/'b'),'prompt':'x','evidence_files':['x']}]}))
            with self.assertRaises(WatchdogError):load_plan(p)

    def test_unchanged_existing_artifact_not_complete(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);w=root/'worker';w.mkdir()
            (w/'evidence.out').write_text('old result')
            p=root/'p.json';p.write_text(json.dumps({'project_root':str(root),'tasks':[
                {'id':'x','cwd':str(w),'prompt':'x','evidence_files':['evidence.out'],'timeout_seconds':2,'progress_timeout_seconds':1}]}))
            runtime=Watchdog(load_plan(p),root/'state',[sys.executable,str(SERVER)],allow_writes=False)
            with patch.dict(os.environ,WD_SCENARIO='noevidence'):
                result=asyncio.run(runtime.run())
            self.assertEqual(result['tasks']['x']['status'],'BLOCKED')
