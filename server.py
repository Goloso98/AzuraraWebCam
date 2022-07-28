from http.server import HTTPServer, BaseHTTPRequestHandler
from requests import get
import re

def baseURL():
  url = get_playlist_url()
  endurl = url.rindex('/') + 1
  return url[:endurl]

def get_playlist_url():
  res = get('https://surftotal.com/camaras-report/grande-porto-douro-litoral/azurara')
  body = res.text
  match = re.search(r"""<source src="(.*)" type="application\/x-mpegURL">""", body)
  playlisturl = match.group(1)
  return playlisturl

def get_playlist():
  url = get_playlist_url()
  return get(url).content

def get_chunklist():
  baseurl = baseURL()
  playlist = get_playlist().decode('utf-8')
  chunklisturl = playlist.split('\n')[3]
  return get(baseurl + chunklisturl).content

def get_media(path):
  baseurl = baseURL()
  url = baseurl[:-1] + path
  media = get(url).content
  return media

body = ''
with open('template.html', 'rb') as f:
  body = f.read()

class MyHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path.startswith('/playlist'):
      self.send_response(200)
      self.send_header("Content-Type", "application/vnd.apple.mpegurl")
      self.end_headers()
      self.wfile.write(get_playlist())
      return
    if self.path.startswith('/chunklist'):
      self.send_response(200)
      self.send_header("Content-Type", "application/vnd.apple.mpegurl")
      self.end_headers()
      self.wfile.write(get_chunklist())
      return
    if self.path.startswith('/media'):
      self.send_response(200)
      self.send_header("Content-Type", "video/MP2T")
      self.send_header("Cache-Control", "no-cache")
      self.end_headers()
      self.wfile.write(get_media(self.path))
      return
    print('server', self.server)
    print('requestline', self.requestline)
    print(self.server.server_name)
    print(self.server.server_port)
    self.send_response(200)
    self.end_headers()
    # self.wfile.write(str(self.path + '\nroot\n').encode())
    self.wfile.write(body)


httpd = HTTPServer(('0.0.0.0', 1234), MyHandler)
print("0.0.0.0:1234")
httpd.serve_forever()
