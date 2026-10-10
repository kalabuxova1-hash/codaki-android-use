import importlib.util,json,tempfile,time,unittest,io
from unittest.mock import patch
from pathlib import Path

path=Path(__file__).resolve().parents[1]/'src'/'relay'/'agent.py'
agent=None
if path.exists():
    spec=importlib.util.spec_from_file_location('agent',path)
    agent=importlib.util.module_from_spec(spec);spec.loader.exec_module(agent)

class AgentTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(agent,'Phone transport has not been implemented')
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.journal=agent.Journal(Path(self.tmp.name));self.addCleanup(self.journal.close)
        self.calls=[]
    def job(self,**changes):
        j={'id':'job-1','tool':'android_set_text','arguments':{'text':'Привет мир'},'expires_at':time.time()+100};j.update(changes);return j
    def execute(self,name,args):
        self.calls.append((name,args));return {'content':[{'type':'text','text':args.get('text','ok')}],'isError':False}
    def test_duplicate_job_returns_cached_result_without_repeating_input(self):
        j=self.job();a=agent.execute_job(j,self.journal,self.execute);b=agent.execute_job(j,self.journal,self.execute)
        self.assertEqual(a,b);self.assertEqual(len(self.calls),1);self.assertEqual(a[1]['content'][0]['text'],'Привет мир')
    def test_changed_arguments_for_same_id_are_refused(self):
        agent.execute_job(self.job(),self.journal,self.execute)
        r=agent.execute_job(self.job(arguments={'text':'другое'}),self.journal,self.execute)
        self.assertEqual(r[2],'uncertain');self.assertEqual(len(self.calls),1)
    def test_expired_job_has_no_side_effect(self):
        r=agent.execute_job(self.job(expires_at=time.time()-1),self.journal,self.execute)
        self.assertTrue(r[1]['isError']);self.assertEqual(self.calls,[])
    def test_shell_and_extra_display_are_rejected(self):
        for j in [self.job(tool='root_shell',arguments={'command':'id'}),self.job(tool='android_tap',arguments={'x':1,'y':2,'display':0})]:
            r=agent.execute_job(j,self.journal,self.execute);self.assertTrue(r[1]['isError'])
        self.assertEqual(self.calls,[])
    def test_uncertain_socket_outcome_blocks_future_jobs(self):
        def fail(*a):raise agent.Uncertain('Core connection lost')
        r=agent.execute_job(self.job(),self.journal,fail);self.assertEqual(r[2],'uncertain')
        r=agent.execute_job(self.job(id='job-2'),self.journal,self.execute)
        self.assertEqual(self.calls,[]);self.assertTrue(r[1]['isError'])
    def test_crash_after_journal_start_blocks_replay_on_restart(self):
        j=self.job();self.journal.start(j,'fingerprint');self.journal.close()
        self.journal=agent.Journal(Path(self.tmp.name));self.addCleanup(self.journal.close)
        r=agent.execute_job(self.job(id='job-2'),self.journal,self.execute)
        self.assertTrue(r[1]['isError']);self.assertEqual(self.calls,[])
    def test_png_is_forwarded_as_mcp_image(self):
        result={'content':[{'type':'image','mimeType':'image/png','data':'iVBORw0KGgo='}],'isError':False}
        r=agent.execute_job(self.job(tool='android_capture',arguments={}),self.journal,lambda *a:result)
        self.assertEqual(r[1],result)
    def test_uncertain_batch_keeps_partial_trace(self):
        partial={'content':[{'type':'text','text':json.dumps({'ok':False,'completed':2,'error':'outcome unknown','trace':[{'op':'tap','result':{'ok':True}}]})}],'isError':True}
        def fail(*a):
            ex=agent.Uncertain('Core timeout');ex.result=partial;raise ex
        r=agent.execute_job(self.job(),self.journal,fail)
        self.assertEqual(r[2],'uncertain');self.assertEqual(r[1]['content'][0],partial['content'][0]);self.assertTrue(self.journal.blocked())
    def test_error_receipt_does_not_mark_result_delivered(self):
        self.assertTrue(hasattr(agent,'deliver_result'),'Delivery acknowledgement validation missing')
        ident,result,status=agent.execute_job(self.job(),self.journal,self.execute)
        class FakeRelay:
            def request(self,*a,**k):return {'error':'temporary database failure'}
        with self.assertRaises(ValueError):agent.deliver_result(FakeRelay(),self.journal,ident,result,status)
        self.assertEqual(len(self.journal.pending()),1)
    def test_private_site_service_access_uses_bearer_header(self):
        self.assertTrue(hasattr(agent.Relay,'close'),'Persistent HTTPS transport lifecycle is missing')
        received=[]
        class Response:
            status=204;will_close=False
            def read(self,*a):return b''
            def close(self):pass
        class Connection:
            def __init__(self,*a,**k):pass
            def request(self,method,path,body=None,headers=None):received.append(headers)
            def getresponse(self):return Response()
            def close(self):pass
        with patch('urllib.request.getproxies',return_value={}):
            relay=agent.Relay({'relay_url':'https://relay.example','agent_token':'a'*64,'sites_authorization':'service-access-token'},connection_factory=Connection)
        self.assertIsNone(relay.request('/agent/jobs/next'))
        self.assertEqual(received[0]['OAI-Sites-Authorization'],'Bearer service-access-token')
    def test_repeated_requests_reuse_https_connection(self):
        self.assertTrue(hasattr(agent.Relay,'close'),'Persistent HTTPS transport lifecycle is missing')
        opened=[];requests=[]
        class Response:
            status=200;will_close=False
            def read(self,*a):return b'{"ok":true}'
            def close(self):pass
        class Connection:
            def __init__(self,host,port,**kwargs):
                opened.append((host,port,kwargs['context'].verify_mode))
            def request(self,method,path,body=None,headers=None):requests.append((method,path))
            def getresponse(self):return Response()
            def close(self):pass
        with patch('urllib.request.getproxies',return_value={}):
            relay=agent.Relay({'relay_url':'https://relay.example','agent_token':'a'*64,'sites_authorization':'access'},connection_factory=Connection)
        self.assertEqual(relay.request('/agent/jobs/next'),{'ok':True})
        self.assertEqual(relay.request('/agent/jobs/job-1/result',{'result':{},'status':'completed'}),{'ok':True})
        self.assertEqual(len(opened),1);self.assertEqual(len(requests),2)
        self.assertEqual(opened[0][2],agent.ssl.CERT_REQUIRED)
    def test_connection_failure_is_not_automatically_replayed(self):
        self.assertTrue(hasattr(agent.Relay,'close'),'Persistent HTTPS transport lifecycle is missing')
        attempts=[]
        class Connection:
            def __init__(self,*a,**k):pass
            def request(self,*a,**k):attempts.append(1);raise OSError('Lost connection')
            def close(self):pass
        with patch('urllib.request.getproxies',return_value={}):
            relay=agent.Relay({'relay_url':'https://relay.example','agent_token':'a'*64,'sites_authorization':'access'},connection_factory=Connection)
        with self.assertRaises(OSError):relay.request('/agent/jobs/next')
        self.assertEqual(len(attempts),1)
    def test_session_setup_is_valid_inside_a_batch(self):
        try:agent.validate_call('android_batch',{'steps':[{'op':'privileges'},{'op':'start'},{'op':'stop'}]})
        except ValueError as exc:self.fail(str(exc))

if __name__=='__main__':unittest.main()
