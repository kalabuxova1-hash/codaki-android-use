#!/usr/bin/env python3
"""Build the public Codex setup ZIP without phone credentials or Git metadata."""
import hashlib
from pathlib import Path
import zipfile

VERSION='0.0.2'
PREFIX='android-use-'+VERSION
ROOT_FILES={'README.md','README.ru.md','INSTALL_WITH_CODEX.md','AGENTS.md','LICENSE',
            'install_with_codex.py','package.json','.gitignore','.gitattributes','CHANGELOG.md'}
DIRECTORIES=('src','magisk','server','scripts','tests','docs','.github','.openai')
SUFFIXES={'.py','.java','.jar','.json','.sh','.mjs','.js','.md','.yml','.yaml','.prop'}

def source_files(root):
    root=Path(root).resolve();names=[]
    candidates=[root/name for name in ROOT_FILES]
    for directory in DIRECTORIES:
        candidates.extend((root/directory).rglob('*'))
    for path in candidates:
        if not path.is_file():continue
        relative=path.relative_to(root).as_posix()
        parts=path.relative_to(root).parts
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise RuntimeError('Refusing a file outside the public source tree')
        if any(part in ('__pycache__','private','.git','node_modules') for part in parts):continue
        if path.name=='config.json' or path.name.startswith(('credentials','.env')):continue
        if relative not in ROOT_FILES and path.suffix not in SUFFIXES:continue
        names.append(relative)
    return sorted(set(names))

def public_bytes(path):
    raw=path.read_bytes()
    if path.suffix=='.jar':return raw
    text=raw.decode('utf-8').replace('\r\n','\n')
    return text.encode('utf-8')

def build(root,output):
    root=Path(root).resolve();output=Path(output);output.mkdir(parents=True,exist_ok=True)
    archive=output/('android-use-codex-setup-'+VERSION+'.zip')
    names=source_files(root)
    required={'INSTALL_WITH_CODEX.md','install_with_codex.py','src/core/display-engine.jar',
              'src/core/ui-test.jar','magisk/module.prop','server/index.js','.openai/hosting.json'}
    if not required.issubset(names):raise RuntimeError('Public setup source is incomplete')
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as bundle:
        for name in names:
            info=zipfile.ZipInfo(PREFIX+'/'+name,date_time=(2026,10,10,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            bundle.writestr(info,public_bytes(root/name))
    instruction=output/'INSTALL_WITH_CODEX.md'
    instruction.write_bytes(public_bytes(root/'INSTALL_WITH_CODEX.md'))
    files=(archive,instruction)
    (output/'SHA256SUMS').write_text(''.join(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+path.name+'\n' for path in files),encoding='ascii',newline='\n')
    return archive

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    print(build(root,root/'release'))
