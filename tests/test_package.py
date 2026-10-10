import importlib.util,json,tempfile,unittest,zipfile,hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'scripts/package.py'
package=None
if source.exists():
    spec=importlib.util.spec_from_file_location('release_package',source)
    package=importlib.util.module_from_spec(spec);spec.loader.exec_module(package)

class PackageTests(unittest.TestCase):
    def setUp(self): self.assertIsNotNone(package,'Release packager is not implemented')
    def test_release_contains_phone_server_and_codex_instruction(self):
        with tempfile.TemporaryDirectory() as d:
            output=package.build(ROOT,Path(d))
            with zipfile.ZipFile(output) as archive:
                names=archive.namelist()
                for name in ['INSTALL_WITH_CODEX.md','install_with_codex.py','src/core/ui-test.jar','src/relay/agent.py','server/index.js','.openai/hosting.json']:
                    self.assertIn(package.PREFIX+'/'+name,names)
                for name in names:
                    self.assertNotIn('..',Path(name).parts)
                    self.assertNotIn('.git',Path(name).parts)
                    self.assertFalse(name.endswith(('.log','.sqlite3','.pyc','config.json')))
                manifest=json.loads(archive.read(package.PREFIX+'/.openai/hosting.json'))
                self.assertIsNone(manifest['project_id'])
    def test_checksum_matches_archive_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            output=package.build(ROOT,Path(d))
            lines=(Path(d)/'SHA256SUMS').read_text().splitlines()
            expected=next(line.split()[0] for line in lines if line.endswith(output.name))
            self.assertEqual(expected,hashlib.sha256(output.read_bytes()).hexdigest())
    def test_archive_contains_every_preserved_runtime_file(self):
        expected=json.loads((ROOT/'docs/preserved-runtime.json').read_text())
        with tempfile.TemporaryDirectory() as d:
            with zipfile.ZipFile(package.build(ROOT,Path(d))) as archive:
                for name,digest in expected.items():
                    with self.subTest(name=name):
                        path=package.PREFIX+'/'+name
                        self.assertIn(path,archive.namelist())
                        self.assertEqual(hashlib.sha256(archive.read(path)).hexdigest(),digest)
    def test_private_config_is_excluded_even_inside_an_allowed_directory(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'src/relay').mkdir(parents=True)
            (root/'src/relay/config.json').write_text('{"agent_token":"DO_NOT_PUBLISH"}')
            self.assertNotIn('src/relay/config.json',package.source_files(root))
    def test_verified_runtime_and_workarounds_match_manifest(self):
        expected=json.loads((ROOT/'docs/preserved-runtime.json').read_text())
        for name,digest in expected.items():
            raw=(ROOT/name).read_bytes()
            if not name.endswith('.jar'):raw=raw.decode('utf-8').replace('\r\n','\n').encode('utf-8')
            with self.subTest(name=name): self.assertEqual(hashlib.sha256(raw).hexdigest(),digest)

if __name__=='__main__':unittest.main()
