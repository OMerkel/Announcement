"""Announcement SMTP based library.

The announcement SMTP based library with a simplified command line startup.

MIT licensed, Copyright (c) 2015
@author Oliver Merkel, Merkel(dot)Oliver(at)web(dot)de.
All rights reserved.
"""
from announcementconfig import *

from smtplib import SMTP
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formataddr
from email.utils import COMMASPACE
from base64 import encodebytes
import os
import getpass

class Announcement:
  FROM = 'From'
  TO = 'To'
  CC = 'CC'
  REPLYTO = 'Reply-To'
  SUBJECT = 'Subject'
  BODY = 'Body'
  SIGNATURE = 'Signature'
  FRIENDLYNAME = 'Friendly Name'
  PATH = 'path'
  MAIL = 'Mail'
  ATTACHMENTS = 'attachments'
  
  user = None
  mailType = None

  def __init__(self, user, mailType):
    self.setUser(user)
    self.setMailType(mailType)

  def setUser(self, user):
    self.user = user
    self.userData = users[user]
    self.update()

  def setMailType(self, mailType):
    self.mailType = mailType
    self.update()

  def update(self):
    if self.user and self.mailType:
      self.renderHeader()
      self.renderBody()
      self.renderMessage()

  def getShortAddressList(self):
    return self.userData[self.MAIL]

  def getFullAddressList(self):
    return [ '"%s" <%s>' % (self.userData[self.FRIENDLYNAME], x) \
      for x in self.getShortAddressList() ]

  def renderBody(self):
    signature = '\n'.join(self.userData[self.SIGNATURE])
    body = '\n'.join(mail[self.mailType][self.BODY])
    body = Template(body).safe_substitute(current)
    self.body = Template(body).safe_substitute(signature=signature)

  def getSubject(self):
    return Template(mail[self.mailType][self.SUBJECT]).safe_substitute(current)

  def renderHeader(self):
    result = {}
    result[self.SUBJECT] = self.getSubject()
    result[self.TO] = mail[self.mailType][self.TO]
    result[self.CC] = mail[self.mailType][self.CC]
    self.header = result

  def renderMessage(self):
    msg = MIMEMultipart('alternative')
    msg[self.SUBJECT] = self.header[self.SUBJECT]
    msg[self.FROM] = self.getFullAddressList()[0]
    msg[self.TO] = COMMASPACE.join(self.header[self.TO])
    msg[self.CC] = COMMASPACE.join(self.header[self.CC])
    msg[self.REPLYTO] = common['replymailaddr']
    partHtml = MIMEText(self.body, 'html')
    msg.attach(partHtml)
    self.message = msg

  def sendMail( self, password ):
    with SMTP( common['mailserver'], 587 ) as smtp:
      smtp.set_debuglevel(1)
      smtp.ehlo()
      smtp.starttls()
      smtp.ehlo()
      smtp.login( self.getShortAddressList()[0], password )
      smtp.sendmail( self.message[self.FROM],
        self.header[self.TO] + self.header[self.CC], self.message.as_string() )

  def sendTestMail(self):
    to = COMMASPACE.join( self.userData[self.MAIL] )
    with SMTP( common['mailserver'] ) as smtp:
      smtp.sendmail( self.message[self.FROM], to, self.message.as_string() )

  def getAttachmentKey( self ):
    return mail[self.mailType][self.ATTACHMENTS] if self.ATTACHMENTS in mail[self.mailType].keys() else None

  def attachmentsMissing( self ):
    result = False
    key = self.getAttachmentKey()
    if not key is None:
      for filePath in current[key]:
        fileName = filePath.split('\\')[-1]
        if not os.path.exists(filePath) or not os.path.isfile(filePath):
          print('Error: Missing %s ( %s )' % (fileName, filePath))
          result = True
    return result

  def attach(self):
    result = True
    key = self.getAttachmentKey()
    if not key is None:
      for filePath in current[key]:
        fileName = filePath.split('\\')[-1]
        if os.path.exists(filePath) and os.path.isfile(filePath):
          fh = open(filePath,'rb')
          part = MIMEBase('application', "octet-stream")
          part.set_payload(encodebytes(fh.read()).decode())
          fh.close()
          part.add_header('Content-Transfer-Encoding', 'base64')
          part.add_header('Content-Disposition', 'attachment; filename="%s"' % fileName)
          self.message.attach(part)    
        else:
          print('Error: Missing %s ( %s )' % (fileName, filePath))
          result = False
    return result
    
if '__main__' == __name__:
  import argparse
  userList = sorted(list(users.keys()))
  mailTypeList = sorted(list(mail.keys()))
  parser = argparse.ArgumentParser(description='Announcement Mailer.')
  parser.add_argument('-u', '--user', nargs=1, type=str,
    choices=userList, default=[userList[0]],
    help='User to send the announcement. ' +
    'Default is to use ' + userList[0])
  parser.add_argument('-t', '--type', nargs=1, type=str,
    choices=mailTypeList, default=[mailTypeList[0]],
    help='Mail type of announcement. ' +
    ('Default is to use "%s"' % mailTypeList[0]))
  parser.add_argument('-s', '--send', nargs=1, type=str,
    choices=['console', 'test', 'serious'],
    default=['console'], help="""How and where to send output.
    "console" shows the mail on console only.
    "test" fakes mail by sending to own mail address only.
    "serious" sends out real mail.
    Default is to use console""" )
  args = parser.parse_args()
  user = args.user[0]
  sendOutput = args.send[0]
  mailType = args.type[0]
  announcement = Announcement(user, mailType)
  if 'console' == sendOutput:
    print(announcement.message.as_string())
  else:
    if announcement.attach():
      if 'test' == sendOutput:
        announcement.sendTestMail()
      else:
        password = getpass.getpass('Hello %s. Please enter your password: ' % self.user).strip()
        announcement.sendMail(password)
    else:
      print("Error: could not include attachments")
