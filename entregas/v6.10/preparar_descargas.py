#!/usr/bin/env python3
"""Reconstruct the exact verified APK and check every release file before upload."""
from pathlib import Path
import hashlib,json,argparse,shutil
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);out=parser.parse_args().out;out.mkdir(parents=True,exist_ok=True)
manifest=json.loads((root/'manifest.json').read_text())
for name,expected in manifest.items():
 if Path(name).name!=name:raise ValueError('Invalid manifest filename')
 target=out/name
 if name.endswith('.apk'):
  with target.open('wb') as dest:
   for index in [1,2]:
    with (root/(name+f'.part{index:02d}')).open('rb') as source:shutil.copyfileobj(source,dest)
 else:shutil.copyfile(root/name,target)
 digest=hashlib.sha256()
 with target.open('rb') as source:
  for block in iter(lambda:source.read(1024*1024),b''):digest.update(block)
 if target.stat().st_size!=expected['bytes'] or digest.hexdigest()!=expected['sha256']:raise ValueError('Integrity error: '+name)
 print('SHA256 OK:',name)
shutil.copyfile(root/'SHA256SUMS.txt',out/'SHA256SUMS.txt')
