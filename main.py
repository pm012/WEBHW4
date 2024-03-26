from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote_plus
from datetime import datetime
import os
import mimetypes
import json
import socket
import threading

HOST = "0.0.0.0"

class SocketServer():
    
    def __init__(self, host, port, event):
        self.host = host
        self.port = port
        self.event = event
        storage_dir = 'storage'
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

        data_file = os.path.join(storage_dir, 'data.json')
        if not os.path.exists(data_file):
            with open(data_file, 'w') as file:
                print('Before writing to file{data_file}')
                json.dump({}, file)
                print("The data is added to file")


    
    def socket_receive(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((self.host, self.port))
        # server_socket.listen(2) - works only in TCP mode
        self.event.set() # Notify the socket server is running        
        
        while True:
            #conn, address = server_socket.accept()
            data, address = server_socket.recvfrom(1024)
            print(f'Received message from {address}: {data.decode()}')
            self.save_to_json(data)

    def save_to_json(self, raw_data):
        storage_path = "./storage/data.json"
        dict_data_timestamp = {}
        if  os.path.exists(storage_path):
            with open(storage_path, 'r',encoding='utf-8') as file:
                dict_data_timestamp=json.loads(file.read())            

        data = unquote_plus(raw_data.decode())
        dict_data = {key: value for key, value in [el.split("=") for el in data.split("&")]}
        dict_data_timestamp[str(datetime.now())] = dict_data        
        with open(storage_path, 'w', encoding="utf-8") as file:
            json.dump(dict_data_timestamp, file, indent=4)


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        #print(f"{self.headers.get('Content-Length')}")
        data = self.rfile.read(int(self.headers.get('Content-Length')))
        self.send_to_server(data)
        print(f"{unquote_plus(data.decode())=}")
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
        


    def do_GET(self):
        pr_url = urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')        
        else:            
            file_path = os.path.join(os.getcwd(), pr_url.path[1:])
            if os.path.exists(file_path):

                self.send_static_file(str(file_path))
            else:
                self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())            

    def send_static_file(self, filename):               
        with open(filename, 'rb') as file:
            self.send_response(200)
            mt = mimetypes.guess_type(self.path)
            self.send_header('Content-type', mt[0])
            self.end_headers()
            self.wfile.write(file.read())

    def send_to_server(self, raw_data):
        host = HOST #socket.gethostname()
        port = 5000

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.connect((host, port))
        client_socket.send(raw_data)
        client_socket.close()
        
def start_http_server(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('0.0.0.0', 3000)
    http = server_class(server_address, handler_class)
    try:
        if event:
            event.wait() # ------
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

def start_socket_server(event):
    socket_server = SocketServer(HOST, 5000, event)
    socket_server.socket_receive()


if __name__ == '__main__':
    event = threading.Event()
    http_thread = threading.Thread(target=start_http_server)
    socket_thread = threading.Thread(target=start_socket_server, args=(event,))

    socket_thread.start()
    event.wait() # Wait until the socket server is running
    http_thread.start()
    

    http_thread.join()
    socket_thread.join()
    


