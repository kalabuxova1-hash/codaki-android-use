import shutil,subprocess,tempfile,unittest
from pathlib import Path

class UiReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which('javac') or not shutil.which('java'):raise unittest.SkipTest('Java runtime is required for UiAutomation adapter tests')
        cls.temp=tempfile.TemporaryDirectory();cls.directory=Path(cls.temp.name)
        sources={
            'com/android/uiautomator/testrunner/UiAutomatorTestCase.java':'package com.android.uiautomator.testrunner; public class UiAutomatorTestCase {}',
            'android/accessibilityservice/AccessibilityServiceInfo.java':'package android.accessibilityservice; public class AccessibilityServiceInfo { public int flags; }',
            'com/oai/androiduse/ReadinessTest.java':'''package com.oai.androiduse;
import java.util.*;
import android.accessibilityservice.AccessibilityServiceInfo;
public class ReadinessTest {
 public static class Window {
  int id; Window(int id){this.id=id;}
  public int getDisplayId(){return id;}
  public Object getRoot(){if(id==0)throw new AssertionError("Physical window was read");return this;}
 }
 public static class Windows {
  int calls,readyAfter; Windows(int readyAfter){this.readyAfter=readyAfter;}
  public int size(){return 2;}
  public int keyAt(int i){return i==0?0:3;}
  public Object get(int id){calls++;return id==3 && calls>=readyAfter?Arrays.asList(new Window(0),new Window(3)):Collections.emptyList();}
 }
 public static class Automation {
  Windows windows;AccessibilityServiceInfo info=new AccessibilityServiceInfo();
  Automation(int readyAfter){windows=new Windows(readyAfter);}
  public AccessibilityServiceInfo getServiceInfo(){return info;}
  public void setServiceInfo(AccessibilityServiceInfo info){this.info=info;}
  public Windows getWindowsOnAllDisplays(){return windows;}
 }
 public static void main(String[] args)throws Exception {
  String mode=args[0];Automation automation=new Automation(mode.equals("ready")?1:mode.equals("delayed")?3:100000);
  long start=System.nanoTime();List<Object> roots=new VirtualUiTest().roots(automation,3);
  long ms=(System.nanoTime()-start)/1000000;
  if(mode.equals("ready") && (ms>=500 || roots.size()!=1))throw new AssertionError("Ready windows unnecessarily wait: "+ms+"ms");
  if(mode.equals("delayed") && (roots.size()!=1 || automation.windows.calls<3 || ms>=600))throw new AssertionError("Window readiness was not polled");
  if(mode.equals("missing") && (!roots.isEmpty() || ms>1600))throw new AssertionError("Missing windows did not time out");
 }
}'''}
        paths=[]
        for name,content in sources.items():
            path=cls.directory/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content);paths.append(str(path))
        source=Path(__file__).resolve().parents[1]/'src'/'java'/'VirtualUiTest.java'
        result=subprocess.run(['javac','--release','8','-d',str(cls.directory),*paths,str(source)],capture_output=True,text=True)
        if result.returncode:raise RuntimeError(result.stderr)
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def check(self,mode):
        result=subprocess.run(['java','-cp',str(self.directory),'com.oai.androiduse.ReadinessTest',mode],capture_output=True,text=True,timeout=5)
        self.assertEqual(result.returncode,0,result.stderr)
    def test_ready_window_returns_without_fixed_delay(self):self.check('ready')
    def test_late_window_is_polled_until_ready(self):self.check('delayed')
    def test_missing_window_has_bounded_wait(self):self.check('missing')

if __name__=='__main__':unittest.main()
