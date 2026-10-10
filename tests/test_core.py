import importlib.util,socketserver,tempfile,unittest
from pathlib import Path
from unittest.mock import patch

source=Path(__file__).resolve().parents[1]/'src'/'core'/'controller.py'
spec=importlib.util.spec_from_file_location('core',source);core=importlib.util.module_from_spec(spec)
with patch.object(socketserver,'ThreadingUnixStreamServer',getattr(socketserver,'ThreadingUnixStreamServer',socketserver.ThreadingTCPServer),create=True):
    spec.loader.exec_module(core)

class CoreTests(unittest.TestCase):
    def test_display_without_destroy_on_removal_is_refused(self):
        fixture='''DisplayDeviceInfo{"AndroidUseCore": uniqueId="virtual:android,0,AndroidUseCore,0", FLAG_TRUSTED, FLAG_OWN_FOCUS, FLAG_OWN_DISPLAY_GROUP, FLAG_ALWAYS_UNLOCKED, FLAG_STEAL_TOP_FOCUS_DISABLED}
  Display 3:
    mPrimaryDisplayDevice=AndroidUseCore(virtual:android,0,AndroidUseCore,0)
    mBaseDisplayInfo=DisplayInfo{"AndroidUseCore", FLAG_TRUSTED, FLAG_OWN_DISPLAY_GROUP, type VIRTUAL}
'''
        with self.assertRaises(core.Denied):core.find_display(fixture)
        self.assertEqual(core.find_display(fixture.replace('FLAG_TRUSTED, FLAG_OWN_FOCUS','FLAG_TRUSTED, FLAG_DESTROY_CONTENT_ON_REMOVAL, FLAG_OWN_FOCUS')),3)
    def reused_pid(self,directory):
        root=Path(directory);pid=root/'engine.pid';pid.write_text('123')
        cmd=root/'proc'/'123'/'cmdline';cmd.parent.mkdir(parents=True);cmd.write_bytes(b'another-process\x00')
        return root,pid
    def test_reused_owner_pid_record_is_cleared_only_when_display_is_absent(self):
        with tempfile.TemporaryDirectory() as directory:
            root,pid=self.reused_pid(directory)
            with patch.object(core,'ENGINE_PID',pid),patch.object(core,'Path',side_effect=lambda value:root/'proc' if value=='/proc' else Path(value)),patch.object(core,'run',return_value='DisplayDeviceInfo{"Screen", type INTERNAL}'):
                self.assertIsNone(core.engine_pid())
            self.assertFalse(pid.exists())
    def test_reused_owner_pid_is_not_accepted_for_an_existing_display(self):
        with tempfile.TemporaryDirectory() as directory:
            root,pid=self.reused_pid(directory)
            with patch.object(core,'ENGINE_PID',pid),patch.object(core,'Path',side_effect=lambda value:root/'proc' if value=='/proc' else Path(value)),patch.object(core,'run',return_value='DisplayDeviceInfo{"AndroidUseCore", invalid flags}'):
                with self.assertRaises(core.Denied):core.engine_pid()
            self.assertTrue(pid.exists())
    def test_reused_owner_pid_record_survives_failed_display_inspection(self):
        with tempfile.TemporaryDirectory() as directory:
            root,pid=self.reused_pid(directory)
            with patch.object(core,'ENGINE_PID',pid),patch.object(core,'Path',side_effect=lambda value:root/'proc' if value=='/proc' else Path(value)),patch.object(core,'find_display',side_effect=core.Denied('Android command timeout')),patch.object(core,'run',side_effect=core.Denied('Android command timeout')):
                with self.assertRaises(core.Denied):core.engine_pid()
            self.assertTrue(pid.exists())
    def test_batch_can_prepare_and_release_session(self):
        calls=[]
        def executor(name,args):calls.append((name,args));return {'ok':True}
        with patch.object(core,'op',side_effect=executor):
            result=core.execute_batch([{'op':'privileges'},{'op':'start'},{'op':'stop'}])
        self.assertTrue(result['ok']);self.assertEqual(len(calls),3)
        self.assertEqual([c[0] for c in calls],['android_privileges','android_start','android_stop'])
    def snapshot(self,nodes):
        self.assertTrue(hasattr(core,'sanitize_ui_snapshot'),'Compact UI snapshots are not implemented')
        return core.sanitize_ui_snapshot({'display':3,'windows':1,'nodes':nodes},3)
    def test_compact_ui_keeps_visible_labels_and_removes_empty_offscreen_nodes(self):
        nodes=[{'text':'null','desc':'null','class':'android.widget.FrameLayout','bounds':[0,1280,0,1280],'clickable':True},
               {'text':'Настройки','desc':'null','class':'android.widget.TextView','bounds':[20,50,250,100],'clickable':False,'editable':False},
               {'text':'Скрытый пункт','bounds':[10,1300,300,1400],'clickable':True}]
        result=self.snapshot(nodes)
        self.assertEqual(len(result['nodes']),1);self.assertEqual(result['nodes'][0]['text'],'Настройки')
        self.assertNotIn('desc',result['nodes'][0])
    def test_compact_ui_never_includes_password_fields(self):
        result=self.snapshot([{'text':'fake-password','password':True,'editable':True,'bounds':[0,0,10,10]}])
        self.assertEqual(result['nodes'],[])
    def test_compact_ui_rejects_a_physical_display_snapshot(self):
        self.assertTrue(hasattr(core,'sanitize_ui_snapshot'),'Compact UI snapshots are not implemented')
        with self.assertRaises(core.Denied):core.sanitize_ui_snapshot({'display':0,'nodes':[]},3)
    def test_partial_failure_preserves_completed_actions_and_does_not_continue(self):
        calls=[]
        def executor(name,args):
            calls.append(name)
            if name=='android_set_text':raise core.Denied('outcome unknown')
            return {'ok':True}
        with patch.object(core,'op',side_effect=executor):
            result=core.execute_batch([{'op':'start'},{'op':'set_text','text':'пример'},{'op':'stop'}])
        self.assertFalse(result['ok']);self.assertEqual(result['completed'],1)
        self.assertEqual(calls,['android_start','android_set_text']);self.assertEqual(len(result['trace']),1)

if __name__=='__main__':unittest.main()
