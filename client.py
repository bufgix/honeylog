from datetime import datetime
import socket
import sys
import pathlib
import logging

PACKET_SIZE = 1024 * 10

logging.basicConfig(level=logging.DEBUG)

HOST, PORT = "".join(sys.argv[1:]).split(':')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    logging.info(f"Connecting {HOST}...")    
    sock.connect((HOST, int(PORT)))
    received = str(sock.recv(PACKET_SIZE), "utf-8")

    now = datetime.now().strftime("%H_%M_%S")
    filename = f"honeylog_{now}.log"
    logfile = pathlib.Path(filename)
    logfile.write_text(received)
    logging.info(f"Saved log file: {filename}")

finally:
    sock.close()