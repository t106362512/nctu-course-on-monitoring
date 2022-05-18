import http.server
import time
import random
from prometheus_client import start_http_server
from prometheus_client import Histogram

REQUEST_LATENCY = Histogram('myapp_latency_seconds', 'Demo histogram metric to record request latency')

class DemoHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    start = time.time()

    # sleep 0 ~ 1 second
    sleep_time = random.random()
    time.sleep(sleep_time)

    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"OK.")

    end = time.time()
    # instrument metric
    REQUEST_LATENCY.observe(end - start)

if __name__ == "__main__":
  print("Starting metrics endpoint...")
  # expose /metrics http endpoint in port 8123
  start_http_server(8123)

  print("Starting service endpoint...")
  # service endpoint
  server = http.server.HTTPServer(('', 8000), DemoHandler)
  server.serve_forever()