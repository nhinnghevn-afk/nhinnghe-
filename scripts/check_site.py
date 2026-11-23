"""Check the portable website; no generated files, no network calls."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist'
class Doc(HTMLParser):
 def __init__(self,text):super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
errors=[];pages=[]
for p in sorted(D.rglob('index.html')):
 text=p.read_text(encoding='utf-8')
 if 'http-equiv="refresh"' in text:continue
 pages.append(p);doc=Doc(text);ids=[a['id'] for t,a in doc.tags if 'id' in a]
 if len(ids)!=len(set(ids)):errors.append(f'Duplicate IDs: {p.relative_to(D)}')
 for tag in ['main','h1']:
  if sum(t==tag for t,a in doc.tags)!=1:errors.append(f'Expected one {tag}: {p.relative_to(D)}')
 for t,a in doc.tags:
  if t not in ['a','script','link','img']:continue
  u=urlsplit(a.get('href',a.get('src','')))
  if u.scheme or u.netloc:continue
  target=(D/u.path.lstrip('/') if u.path.startswith('/') else p.parent/u.path) if u.path else p
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'Missing target: {p.relative_to(D)} -> {u.path}')
  elif u.fragment and target.suffix=='.html':
   target_ids={a.get('id') for t,a in Doc(target.read_text(encoding='utf-8')).tags}
   if unquote(u.fragment) not in target_ids:errors.append(f'Missing anchor: {p.relative_to(D)} -> {u.path}#{u.fragment}')
x=json.loads((D/'school-public-data.json').read_text(encoding='utf-8'));c=x['careers']
if len(c)!=25 or len(x['majors'])!=57:errors.append('Expected 25 careers and 57 major summaries.')
if sum(v.get('profileKind')=='sample' for v in c)!=1 or sum(v.get('profileKind')=='basic' for v in c)!=24:errors.append('Expected 1 sample + 24 basic profiles.')
if len(json.loads((D/'school-programs.json').read_text(encoding='utf-8'))['programs'])!=10:errors.append('Expected 10 public programs at export baseline.')
for v in c:
 if not all(v.get(k) for k in ['summary','output','foundation','tryTask','tryResult','majorHints']):errors.append('Incomplete discovery profile: '+v['id'])
if errors:raise SystemExit('FAILED\n'+'\n'.join(errors))
print(f'PASS: {len(pages)} content pages; links/assets/anchors; 25 careers; 57 majors; 10 programs; 1 sample + 24 basic profiles.')
print('External sources and current admissions were not reverified by this offline check.')
