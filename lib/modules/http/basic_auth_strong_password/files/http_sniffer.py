import os
import sys
import datetime
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import base64

# Config
HTTP_ADDR = ''
HTTP_PORT = 80


class StdLogger():
    def __init__(self, logname):
        self.logfile = '/root/logs/'+ logname + '.log'

    def write(self, message):
        f = open(self.logfile, 'a')
        f.write('%s' % (message))
        f.close()

class Logger():
    def __init__(self, logname):
        self.logfile = '/root/logs/'+ logname + '.log'

    def logtime(self):
        now = datetime.datetime.now()
        part1 = now.strftime('%Y-%m-%d %H:%M:%S')
        return part1

    def log(self, *args):
        f = open(self.logfile, 'a')
        ip,port, data= args[0],args[1],args[2]
        if (isinstance(data, str)):
            f.write(
            json.dumps(
                {"IP" : ip ,
                 "PORT": port,'DATA' : data,
                 "module_name" : "http/basic_auth_strong_password", \
                 'date':self.logtime()})
                + "\n")
            f.close()
        else:
            username,password=data[0],data[1]
            f.write(json.dumps(
                {"username": username, "password": password, "IP" : ip ,
                 "PORT": port,
                 "module_name" : "http/basic_auth_strong_password", \
                 'date':self.logtime()})+ "\n")
            f.close()

class RequestHandler(BaseHTTPRequestHandler):
    # Create loggers
    potlogger = Logger('logins')
    accesslogger = Logger('access')
    errorlogger = Logger('error')

    # Get client source port
    def srcport_string(self):
        host, port = self.client_address[:2]
        return port

    #
    # Override BaseHTTPServer
    #

    # Set server header
    server_version = 'Admin Console/1.0'
    sys_version = ''

    # Hide error response body
    error_message_format = ''

    # Change log format
    def log_request(self, code='-', size='-'):
        self.log_message(
             '"%s" %s "%s"',
            self.requestline.replace('"', '\\"'),
            str(code),
            self.headers.get('User-Agent', '').replace('"', '\\"'))

    # Log messages to access.log instead of stderr
    def log_message(self, format, *args):
        self.accesslogger.log(
            self.address_string(),
            self.srcport_string(),
            format%args)

    # Log errors to error.log instead of calling log_message()
    def log_error(self, format, *args):
        self.errorlogger.log(
            self.address_string(),
            self.srcport_string(),
            format%args)

    # Skip name resolving
    def address_string(self):
        host, port = self.client_address[:2]
        return host


    # Request handling
    def do_HEAD(self):
        # Always send 401 response
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="ADMIN"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Decode and log credentials, if any.
        authstring = self.headers.get('Authorization', None)
        if authstring != None:
            authparts = authstring.split()
            if len(authparts) == 2 and authparts[0] == 'Basic':
                try:
                    authdecoded = base64.b64decode(authparts[1])
                    authdecoded=authdecoded.decode('utf-8')
                except TypeError as e:
                    self.errorlogger.log(
                        self.address_string(),
                        self.srcport_string(),
                        authparts[1])
                else:
                    self.potlogger.log(
                        self.address_string(),
                        self.srcport_string(),
                        authdecoded.split(":",1))

    # GET = HEAD
    def do_GET(self):
        self.do_HEAD()

# Main
def main():
    # Redirect stdout and stderr
    stdlog = StdLogger('logins')
    outsave = sys.stdout
    errsave = sys.stderr
    sys.stdout = stdlog
    sys.stderr = stdlog

    # Start listener
    httpd = HTTPServer(
        (HTTP_ADDR, HTTP_PORT), RequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

    # Restore stdout and stderr
    sys.stdout = outsave
    sys.stderr = errsave

if __name__ == '__main__':
    main()
