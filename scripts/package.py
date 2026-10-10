#!/usr/bin/env python3
"""Build the public Codex setup ZIP without phone credentials or Git metadata."""
import hashlib
import importlib.util
from pathlib import Path
import zipfile

VERSION='0.0.3'
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('android_use_card',ROOT/'chatgpt'/'package_card.py')
card_builder=importlib.util.module_from_spec(spec)
spec.loader.exec_module(card_builder)
PREFIX='android-use-'+VERSION
ROOT_FILES={'README.md','README.ru.md','INSTALL_WITH_CODEX.md','AGENTS.md','LICENSE',
            'install_with_codex.py','package.json','.gitignore','.gitattributes','CHANGELOG.md'}
DIRECTORIES=('src','magisk','server','scripts','tests','docs','.github','.openai')
SUFFIXES={'.py','.java','.jar','.json','.sh','.mjs','.js','.md','.yml','.yaml','.prop'}

def source_files(root):
    root=Path(root).resolve();names=[]
    candidates=[root/name for name in ROOT_FILES]
    card_files={'chatgpt/package_card.py','chatgpt/README.md'}|{'chatgpt/plugin/'+name for name in card_builder.FILES}
    candidates.extend(root/name for name in card_files)
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
        if relative not in ROOT_FILES|card_files and path.suffix not in SUFFIXES:continue
        names.append(relative)
    return sorted(set(names))

def public_bytes(path):
    raw=path.read_bytes()
    if path.suffix in ('.jar','.png','.zip'):return raw
    text=raw.decode('utf-8').replace('\r\n','\n')
    return text.encode('utf-8')

def build(root,output):
    root=Path(root).resolve();output=Path(output);output.mkdir(parents=True,exist_ok=True)
    archive=output/('android-use-codex-setup-'+VERSION+'.zip')
    card=card_builder.build_card(root,output)
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
        info=zipfile.ZipInfo(PREFIX+'/chatgpt/'+card.name,date_time=(2026,10,10,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o100644<<16
        bundle.writestr(info,card.read_bytes())
    instruction=output/'INSTALL_WITH_CODEX.md'
    instruction.write_bytes(public_bytes(root/'INSTALL_WITH_CODEX.md'))
    files=(archive,instruction,card)
    (output/'SHA256SUMS').write_text(''.join(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+path.name+'\n' for path in files),encoding='ascii',newline='\n')
    return archive

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    print(build(root,root/'release'))
