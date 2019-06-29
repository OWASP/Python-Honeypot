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
        self.logfile = os.path.join(os.path.dirname(__file__), logname) + '.log'

    def write(self, message):
        f = open(self.logfile, 'a')
        f.write('%s' % (message))
        f.close()

class BapLogger():
    def __init__(self, logname):
        self.logfile = os.path.join(os.path.dirname(__file__), logname) + '.log'

    def logtime(self):
        now = datetime.datetime.now()
        part1 = now.strftime('%Y-%m-%d %H:%M:%S')
        part2 = now.strftime('%f')
        # Floor milliseconds
        return '%s,%s' % (part1, part2[:3])

    def log(self, format, *args):
        f = open(self.logfile, 'a')
        f.write(
            json.dumps(
            '[%s] %s\n' % (
            self.logtime(),
                format%args))+ "\n")
        f.close()

class RequestHandler(BaseHTTPRequestHandler):
    # Create loggers
    potlogger = BapLogger('bap')
    accesslogger = BapLogger('access')
    errorlogger = BapLogger('error')

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
            '%s:%s %s',
            self.address_string(),
            self.srcport_string(),
            format%args)

    # Log errors to error.log instead of calling log_message()
    def log_error(self, format, *args):
        self.errorlogger.log(
            '%s:%s %s',
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
                except TypeError as e:
                    self.errorlogger.log(
                        '%s:%s DecodeFailure %s',
                        self.address_string(),
                        self.srcport_string(),
                        authparts[1])
                else:
                    self.potlogger.log(
                        '%s:%s Basic %s',
                        self.address_string(),
                        self.srcport_string(),
                        authdecoded)

    # GET = HEAD
    def do_GET(self):
        self.do_HEAD()

# Main
def main():
    # Redirect stdout and stderr
    stdlog = StdLogger('bap')
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
