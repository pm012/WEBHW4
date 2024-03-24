from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        elif pr_url.path.startswith('/static/'): # Handle static files
            filename = pr_url.path.lstrip('/static/')
            self.send_static_file(filename)
        else:
            self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())            

    def send_static_file(self, filename):
        static_dir = os.path.join(os.getcwd(), 'static') # Assuming static files are in a 'static' direcroty
        filepath = os.path.join(static_dir, filename)
        if os.path.exists(filepath) and os.path.isfile(filepath):
            with open(filepath, 'rb') as file:
                self.send_response(200)
                if filename.lower().endswith('.png'):
                    self.send_header('Content-type', 'image/png')
                elif filename.lower().endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                self.end_headers()
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'File Not Found')


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()
    


