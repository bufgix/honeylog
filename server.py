import socketserver
import pathlib
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
logfile = pathlib.Path("".join(sys.argv[1:]))


class TCPHandler(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        self.logfile = logfile
        super().__init__(*args, **kwargs)

    def handle(self):
        logging.info(f"Client connected... ({self.client_address[1]})")
        logging.info(f"Sending {self.logfile}...")
        self.request.sendall(bytes(self.logfile.read_text(), encoding="utf-8"))
        logging.info(f"Success sending file...")



if __name__ == '__main__':
    try:
        server = socketserver.TCPServer(('localhost', 2112), TCPHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        logging.error("Server interrupted")
    