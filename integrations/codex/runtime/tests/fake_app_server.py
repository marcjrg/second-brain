"""Scriptable JSONL stand-in for app-server; intentionally no real Codex service."""
import json, sys, pathlib, time, os

def send(value):
    print(json.dumps(value), flush=True)

thread='thr_fake'
turn='turn_fake'
request = 0
scenario = os.environ.get('WD_SCENARIO', 'success')
for line in sys.stdin:
    try: msg=json.loads(line)
    except Exception: continue
    method=msg.get('method'); ident=msg.get('id')
    if method=='initialize': send({'id':ident,'result':{'userAgent':'fake'}})
    elif method=='initialized': continue
    elif method=='thread/start': send({'id':ident,'result':{'thread':{'id':thread}}})
    elif method=='turn/start':
        send({'id':ident,'result':{'turn':{'id':turn,'status':'inProgress'}}})
        send({'method':'turn/started','params':{'threadId':thread,'turn':{'id':turn}}})
        if scenario=='hang': continue
        if scenario=='approval':
            send({'method':'item/commandExecution/requestApproval','id':999,'params':{'threadId':thread,'turnId':turn,'command':'danger'}})
            continue
        if scenario=='twofail':
            for n in range(2):
                send({'method':'item/completed','params':{'threadId':thread,'turnId':turn,'item':{'id':str(n),'type':'commandExecution','command':'false','cwd':os.getcwd(),'status':'failed','exitCode':1}}})
            continue
        if scenario=='success':
            pathlib.Path('evidence.out').write_text('verified-' + str(time.time_ns()))
            send({'method':'item/completed','params':{'threadId':thread,'turnId':turn,'item':{'id':'1','type':'fileChange','status':'completed','changes':[{'path':'evidence.out','kind':'added'}]}}})
            send({'method':'turn/completed','params':{'threadId':thread,'turn':{'id':turn,'status':'completed'}}})
        elif scenario=='noevidence':
            send({'method':'turn/completed','params':{'threadId':thread,'turn':{'id':turn,'status':'completed'}}})
        elif scenario=='failed':
            send({'method':'turn/completed','params':{'threadId':thread,'turn':{'id':turn,'status':'failed'}}})
        else: raise RuntimeError('unknown scenario')
    elif method=='turn/interrupt':
        send({'id':ident,'result':{}})
        send({'method':'turn/completed','params':{'threadId':thread,'turn':{'id':turn,'status':'interrupted'}}})
    elif ident == 999:
        # Denial response has no method and is consumed here.
        send({'method':'turn/completed','params':{'threadId':thread,'turn':{'id':turn,'status':'interrupted'}}})
