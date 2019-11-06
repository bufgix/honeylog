from datetime import datetime
import socket
import sys
import pathlib
import logging

PACKET_SIZE = 1024

logging.basicConfig(level=logging.DEBUG)

HOST, PORT = "".join(sys.argv[1:]).split(':')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    logging.info(f"Connecting {HOST}...")    
    sock.connect((HOST, int(PORT)))
    now = datetime.now().strftime("%H_%M_%S")
    filename = f"honeylog_{now}.log"
    logfile = pathlib.Path(filename)
    with logfile.open(mode="w") as fid:
        while True:
            recv = str(sock.recv(PACKET_SIZE), "utf-8")
            if not recv:
                break
            fid.write(recv)
    logging.info(f"Saved log file: {filename}")

finally:
    sock.close()