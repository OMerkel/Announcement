"""Announcement SMTP based library.

The announcement SMTP based library with a simplified command line startup.

MIT licensed, Copyright (c) 2015
@author Oliver Merkel, Merkel(dot)Oliver(at)web(dot)de.
All rights reserved.
"""
from announcementconfig import *

import smtplib
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
    self.body = Template(body).substitute(signature=signature)

  def getSubject(self):
    return Template(mail[self.mailType][self.SUBJECT]).substitute(current)

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
    server = smtplib.SMTP( common['mailserver'], 587 )
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login( self.getShortAddressList()[0], password )
    server.sendmail( self.message[self.FROM],
      self.header[self.TO] + self.header[self.CC], self.message.as_string() )
    server.quit()
  
  def sendTestMail(self):
    to = COMMASPACE.join( self.userData[self.MAIL] )
    server = smtplib.SMTP( common['mailserver'] )
    server.sendmail( self.message[self.FROM], to, self.message.as_string() )
    server.quit()

  def attachmentsAvailable( self ):
    result = True
    for path in current[Announcement.ATTACHMENTS]:
      filePath = os.path.join( current[Announcement.PATH], path )
      fileName = path.split('\\')[-1]
      if not os.path.exists(filePath) or not os.path.isfile(filePath):
        print('Error: Missing %s ( %s )' % (fileName, filePath))
        result = False
    return result
  
  def attach(self):
    result = True
    for path in current[Announcement.ATTACHMENTS]:
      filePath = os.path.join( current[Announcement.PATH], path )
      fileName = path.split('\\')[-1]
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
  user = sorted(list(users.keys()))[0]
  mailType = sorted(list(mail.keys()))[0]
  announcement = Announcement(user, mailType)
  print(announcement.message.as_string())
  """
  announcement.attach()
  if True:
    announcement.sendTestMail()
  else:
    password = getpass.getpass('Hello %s. Please enter your password: ' % self.user).strip()
    announcement.sendMail(password)
  """
