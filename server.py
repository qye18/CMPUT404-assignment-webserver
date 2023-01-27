#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
       
        method = self.data.decode('utf-8').split(" ")[0]
        reqPath = self.data.decode('utf-8').split(" ")[1]

        # handle methods, only GET allowed, otherwise return 405
        if method != "GET":
            self.request.sendall(bytearray(f"HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
            return

        # handle end with /
        if reqPath.endswith("/"):
            reqPath += "index.html"
        # correct path ending
        elif not (reqPath.endswith("/") or reqPath.endswith(".html") or reqPath.endswith(".css")):
            redirect_location = reqPath + "/"
            self.request.sendall(bytearray(f"HTTP/1.1 301 Moved Permanently\r\nLocation:{redirect_location}\r\n"))

        try:
            with open("www"+reqPath,"r") as file1:
                file_data = file1.read()
        except:
            # handle file not exists, return 404
            self.request.sendall(bytearray(f"HTTP/1.1 404 Not Found\r\n",'utf-8'))
        else:
            # handle 200
            if (reqPath.endswith(".html")):
                self.request.sendall(bytearray(f"HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n\n{file_data}",'utf-8'))
            elif (reqPath.endswith(".css")):
                self.request.sendall(bytearray(f"HTTP/1.1 200 OK\r\nContent-Type:text/css\r\n\n{file_data}",'utf-8'))
        self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
