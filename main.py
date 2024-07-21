import http.server
import socketserver
import os
from urllib.parse import urlparse, parse_qs
import json
import socket

PORT = 3001

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path).path
        print(f"Handling GET request for: {parsed_path}")

        # Serve files from the web directory
        if parsed_path == '/':
            self.path = 'web/index.html'
        elif parsed_path.startswith('/'):
            self.path = 'web' + parsed_path
        else:
            self.path = 'web/error.html'

        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        print(f"Handling POST request for: {self.path}")
        if self.path == '/message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            print(f"Received POST data: {post_data}")
            data = parse_qs(post_data.decode('utf-8'))
            print(f"Parsed data: {data}")

            message_data = {
                "username": data['username'][0],
                "message": data['message'][0]
            }

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Use 'socket' as the hostname to connect to the 'socket' service
                sock.connect(('socket', 5001))
                sock.sendall(json.dumps(message_data).encode('utf-8'))
                sock.close()
                print("Message sent successfully")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Message sent successfully')
            except Exception as e:
                print(f"Error: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Internal Server Error')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Page not found')

handler_object = MyHttpRequestHandler

my_server = socketserver.TCPServer(("", PORT), handler_object)

print(f"Serving on port {PORT}")
my_server.serve_forever()