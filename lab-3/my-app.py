import http.server
import random
from prometheus_client import start_http_server
from prometheus_client import Counter
from prometheus_client import Gauge

REQUESTS_COUNTER = Counter('myapp_requests', 'Demo counter metric to record request count', labelnames=['path', 'response_code'])

app_info = {
  'app': 'myapp',
  'author' : '310551017 王志嘉',
  'author_email': 'cwang.cs10@nycu.edu.tw',
  'version' : '0.0.1'
}

INFO = Gauge('myapp_info', 'Demo info metric to record application info', 
             labelnames=app_info.keys())
INFO.labels(**app_info).set(1)

class DemoHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    if random.random() <= 0.2:
      # Simulate error
      # instrument metric
      REQUESTS_COUNTER.labels(self.path, 500).inc()

      self.send_response(500)
      self.end_headers()
      self.wfile.write(b"Simulate Error!\n")
    else:
      # instrument metric
      REQUESTS_COUNTER.labels(self.path, 200).inc()

      self.send_response(200)
      self.end_headers()
      self.wfile.write(b"OK.")

if __name__ == "__main__":
  print("Starting metrics endpoint...")
  # expose /metrics http endpoint in port 8123
  start_http_server(8123)

  print("Starting service endpoint...")
  # service endpoint
  server = http.server.HTTPServer(('', 8000), DemoHandler)
  server.serve_forever()