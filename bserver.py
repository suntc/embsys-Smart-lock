import time
import BaseHTTPServer
import urlparse
import sys

from lockObject import lockObject
from send import simcard_task
from servo import servo

HOST_NAME = '127.0.0.1' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 7010 # Maybe set this to 9000.

with open('index.html', 'r') as myfile:
    index = myfile.read().replace('\n', '')

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        ulk = lockObject()
        sv = servo()
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        gv = s.path.split('?')
        print gv
        if (len(gv) > 1):
            print "gv len=" + str(len(gv))
            gvd = urlparse.parse_qs(gv[1])
            if 'uid' in gvd and 'bid' in gvd:
                print gvd['uid'][0], gvd['bid'][0]
                qr = ulk.add_item(gvd['uid'][0], gvd['bid'][0])
                if qr != False:
                    print "http://lo.wows.tech/qrcode/?data=" + qr
                    sim = simcard_task(qr, ulk.users[gvd['uid'][0]]['phone'])
                    sim.start()
                    sv.close()
                    print "add item succeed"
        s.wfile.write(index)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        HOST_NAME = sys.argv[1]
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
