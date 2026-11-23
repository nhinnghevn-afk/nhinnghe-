"""Serve the exported static site from its root; Python 3, no dependencies."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8000);args=parser.parse_args()
root=Path(__file__).resolve().parents[1]/'dist'
handler=partial(SimpleHTTPRequestHandler,directory=str(root))
print(f'Nhìn Nghề: http://127.0.0.1:{args.port}/',flush=True)
try:
 ThreadingHTTPServer(('127.0.0.1',args.port),handler).serve_forever()
except KeyboardInterrupt:
 print('Stopped.')
