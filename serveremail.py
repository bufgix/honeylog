from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
import smtplib
import sys
import pathlib
import argparse
import logging
import time

parser = argparse.ArgumentParser()
parser.add_argument(
    'logpath', help="The file that will send to email", metavar="LOGPATH")
parser.add_argument(
    'gmail', help="Email adress that will receive log file", metavar="GMAIL")
parser.add_argument('passw', help="Password of your gmail", metavar="PASSWORD")
parser.add_argument("--interval", default=10, type=int, help="Interval to the sending process")

logging.basicConfig(level=logging.DEBUG)


def send_email(server, **kwargs):
    now = datetime.now().strftime("%H_%M_%S")

    body = MIMEMultipart()
    body['From'] = kwargs['gmail']
    body['To'] = kwargs['gmail']
    body['Subject'] = f"{now} kippo logfile"

    body.attach(MIMEText(f"{now} kippo logfile"))

    logfile = pathlib.Path(kwargs['logpath'])

    part = MIMEApplication(logfile.read_text())
    part['Content-Disposition'] = f'attachment; filename="{logfile}"'
    body.attach(part)

    logging.info(f"Sending {logfile} to {kwargs['gmail']} ...")

    server.send_message(body)

    logging.info("File sended.")



def main():
    args = parser.parse_args()
    while(True):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(args.gmail, args.passw)
            send_email(server, **vars(args))
            time.sleep(args.interval)
        except KeyboardInterrupt:
            server.quit()
            logging.error("Process interrupted!")
            break
        except smtplib.SMTPAuthenticationError as authex:
            logging.error("Auth error check email or password!")
            break


if __name__ == '__main__':
    main()
