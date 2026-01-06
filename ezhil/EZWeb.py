#!/usr/bin/python
# -*- coding: utf-8 -*-
## 
## (C) 2013 Muthiah Annamalai,
## Licensed under GPL Version 3
## 
## Ezhil language Interpreter via Web

## Ref: http://wiki.python.org/moin/BaseHttpServer

import time
# Web Serving Essentials for CGI and normal http webserver 
import http
from http.server import SimpleHTTPRequestHandler,CGIHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
import cgi, cgitb

from .ezhil import EzhilFileExecuter
# for handling buffer like handling
from contextlib import redirect_stdout
import io
import subprocess
import os

PYTHON3 = os.environ.get("PYTHON3")

if not PYTHON3:
    raise RuntimeError("PYTHON3 environment variable not set")

cgitb.enable()

DEBUG = False


class BaseEzhilWeb(CGIHTTPRequestHandler):
    def do_GET(self): 
        SimpleHTTPRequestHandler.do_GET(self)
        return

    def do_POST(self):
        POSTvars = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
        )
        if 'prog' in POSTvars:
            program = "".join(POSTvars['prog'].value)
        elif 'eval' in POSTvars:
            program = 'printf("Welcome to Ezhil! You can type a program and execute it online!")'
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>HTTP 404 : Error occured</h1>")
            self.wfile.write(str(POSTvars).encode('utf-8'))
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.do_ezhil_execute(program)
        return

        

    def do_ezhil_execute(self, program):
        failed=True
        try:
            result = subprocess.run(
                [PYTHON3,"-m","ezhil.ezhil_runner"],
            input=program,
            text=True,
            capture_output=True,
            timeout=10  # HARD TIMEOUT
            )

            stdout = result.stdout
            stderr = result.stderr

            failed = result.returncode != 0

        except subprocess.TimeoutExpired as e:
            stdout = e.stdout or ""
            stderr = "Execution timed out after 10 seconds"
            failed = True

        if failed:
            op = "<H2> Your program has some errors! </H2><HR/><BR/>"
        else:
            op = "<H2> Your program executed correctly! </H2><HR/><BR/>"
        op += "<pre>{}</pre>".format(stdout or stderr)

        real_op = f"""
        <html>
        <head><title>Ezhil interpreter</title></head>
        <body>{op}</body>
        </html>
        """

        self.wfile.write(real_op.encode("utf-8"))



class EzhilWeb(ThreadingMixIn, BaseEzhilWeb):
    """ Add threading to handle requests in separate thread """
    pass


HOST_NAME = "0.0.0.0"
PORT_NUMBER = 8080

if __name__ == "__main__":
    httpd = http.server.HTTPServer((HOST_NAME, PORT_NUMBER), EzhilWeb)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))
