import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        with open("cruziwords/index.html", "r", encoding='utf-8') as f:
            output = f.read()
        self.wfile.write(output.encode())

    def do_POST(self):
        upload_dir = './cruziwords/examples'

        if self.path.endswith('/cruziwords'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_length = int(self.headers['Content-Length'])
            pdict['CONTENT-LENGTH'] = content_length
            if ctype == 'multipart/form-data':
                multipart_data = cgi.parse_multipart(self.rfile, pdict)
                form_file = multipart_data.get('file')[0]

                fo = open("%s/tmp.csv" % upload_dir, "wb")
                fo.write(form_file)
                fo.close()
                print("File is uploaded to server as tmp.csv file")

            self.send_response(200)
            self.send_header('content-type', 'text/html')
            # self.send_header('Location', '/cruziwords')
            self.end_headers()
            subprocess.call("cruziwords ./cruziwords/examples/tmp.csv --html-out TMP.html", shell=True)
            with open("TMP.html", "r", encoding='utf-8') as f:
                output2 = f.read()
            self.wfile.write(output2.encode())

def main():
    PORT = 8000
    server = HTTPServer(('', PORT), HelloHandler)
    print('Server Running on port %s' % PORT)
    server.serve_forever()


if __name__ == '__main__':
    main()
