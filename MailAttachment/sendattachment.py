#!/usr/bin/env python
'''
  Script name: sendattachment.py

  Functionality:A sample script to send csv attachement using smtplib
  Usage: python sendattachment.py <from_address> <to_address> <file> <subject>
  Example: python drgf@gmail.com abc@gmail.com xyz.txt "testing"

'''

import os
import sys
import smtplib
import mimetypes
import traceback

try :
        from email.mime.multipart import MIMEMultipart
except ImportError:
        from email.MIMEMultipart import MIMEMultipart
try :
        from email import encoders
except ImportError:
        from email import Encoders
try :
        from email.message import Message
except ImportError:
        from email.Message import Message
try :
        from email.mime.base import MIMEBase
except ImportError:
        from email.MIMEBase import MIMEBase
try :
        from email.mime.text import MIMEText
except ImportError:
        from email.MIMEText import MIMEText

class Mail_ins():
        def __init__(self, from_address, to_address, file, subject):
                self.from_address = from_address
                self.to_address = to_address
                self.file = file
                self.subject = subject
        def send_attachment(self):
                msg = MIMEMultipart()
                msg['Subject'] = self.subject
                msg['From'] = self.from_address
                msg['To'] = self.to_address
                msg.preamble = self.subject
                ctype, encoding = mimetypes.guess_type(self.file)
                if ctype is None or encoding is not None:
                    ctype = "application/octet-stream"

                maintype, subtype = ctype.split("/", 1)
                if maintype == "text":
                    fp = open(self.file)
                    attachment = MIMEText(fp.read(), _subtype=subtype)
                    fp.close()
                else:
                    fp = open(self.file, "rb")
                    attachment = MIMEBase(maintype, subtype)
                    attachment.set_payload(fp.read())
                    fp.close()
                try :
                    encoders.encode_base64(attachment)
                except :
                    Encoders.encode_base64(attachment)
                attachment.add_header("Content-Disposition", "attachment", filename=self.file)
                msg.attach(attachment)
                # Send the message via locahost
                s = smtplib.SMTP('localhost')
                s.sendmail(from_address, [to_address], msg.as_string())
                s.quit()

def usage():
        print '''Usage: sendattachment.py <from_address> <to_address> <file> <subject>
        E.g.python  sendattachment.py drgf@gmail.com abc@gmail.com xyz.txt "testing"'''
if __name__== '__main__':
        if len(sys.argv)<4:
                print "Insufficient input arguments"
                usage()
                sys.exit(1)
        try:
            from_address = sys.argv[1]
            to_address = sys.argv[2]
            file = sys.argv[3]
            subject = sys.argv[4]
            hostname = os.uname()[1]
            obj_mail = Mail_ins(from_address, to_address, file, subject)
            obj_mail.send_attachment()
        except:
            print "An error has occured "
            print "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
