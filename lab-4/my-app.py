import http.server
import random
from prometheus_client import start_http_server
from prometheus_client import Counter

REQUESTS_COUNTER = Counter('myapp_requests', 'Demo counter metric to record request count', labelnames=['path', 'response_code'])

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
  print("Done")

  print("Starting service endpoint...")
  # service endpoint
  server = http.server.HTTPServer(('', 8000), DemoHandler)
  server.serve_forever()