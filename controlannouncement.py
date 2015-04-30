"""GUI control in tkinter for the Announcement application.

Used to start the Python/tkinter User Experience interactively.
Some SMTP knowledge will be helpfull.

MIT licensed, Copyright (c) 2015
@author Oliver Merkel, Merkel(dot)Oliver(at)web(dot)de.
All rights reserved.
"""
from announcementconfig import *

from announcement import Announcement
from tkinter import Tk
from tkinter import Frame
from tkinter.ttk import Combobox

from tkinter import Button
from tkinter import Checkbutton
from tkinter import Entry
from tkinter import Label
from tkinter import Toplevel

from tkinter import ACTIVE
from tkinter import DISABLED
from tkinter import END
from tkinter import INSERT
from tkinter import LEFT
from tkinter import NORMAL
from tkinter import W
from tkinter import WORD
from tkinter.scrolledtext import ScrolledText

import sys

class ControlAnnouncement:
  def __init__(self, parent):
    self.announcement = Announcement( sorted(list(users.keys()))[0], sorted(list(mail.keys()))[0] )
    self.initializeGui(parent)

  def initializeGui(self, parent):
    self.parent = parent
    self.frame = Frame(self.parent)
    self.frame.grid(column=0, row=0)

    Label(self.frame, text="User").grid(row=0, sticky=W)
    Label(self.frame, text="Type").grid(row=1, sticky=W)

    userList = sorted(list(users.keys()))
    self.comboBoxUser = Combobox(self.frame, state="readonly", width=20, values=userList)
    self.comboBoxUser.set( userList[0] )
    self.comboBoxUser.grid(row=0, column=1, sticky=W)
    self.comboBoxUser.bind('<<ComboboxSelected>>', self.updateUser)

    announcementTypes = sorted(list(mail.keys()))
    self.comboBoxType = Combobox(self.frame, state="readonly", width=35, values=announcementTypes)
    self.comboBoxType.set( announcementTypes[0] )
    self.comboBoxType.grid(row=1, column=1, sticky=W)
    self.comboBoxType.bind('<<ComboboxSelected>>', self.updateType)

    self.scolledText = ScrolledText(self.frame, wrap = WORD, width  = 80, height = 15)
    self.scolledText.grid(row=2, column=1, columnspan=2)
    self.scolledText.config(state=NORMAL)
    self.scolledText.insert(INSERT, self.announcement.message.as_string())
    self.scolledText.config(state=DISABLED)

    self.buttonSendTestMail=Button(self.frame, text='Send Test Mail', command=self.sendTestMail)
    self.buttonSendTestMail.grid(row=4, column=1)

    self.buttonSendMail=Button(self.frame, text='Send Mail', command=self.sendMail)
    self.buttonSendMail.grid(row=4, column=2)

    self.checkButtonAttachmentAvailable=Checkbutton(self.frame, text="Attachments available")
    self.checkButtonAttachmentAvailable.grid(row=3, sticky=W)

    self.checkAttachments()

  def checkAttachments(self):
    key = self.announcement.getAttachmentKey()
    print("Info: Attachment key is " + str(key))
    self.checkButtonAttachmentAvailable.config(state=NORMAL)
    if key is None:
      self.checkButtonAttachmentAvailable.deselect()
      self.buttonSendTestMail.config(state=NORMAL)
      self.buttonSendMail.config(state=NORMAL)
    else:
      if not self.announcement.attachmentsMissing():
        self.checkButtonAttachmentAvailable.select()
        self.buttonSendTestMail.config(state=NORMAL)
        self.buttonSendMail.config(state=NORMAL)
      else:
        self.checkButtonAttachmentAvailable.deselect()
        # self.buttonSendTestMail.config(state=DISABLED)
        self.buttonSendMail.config(state=DISABLED)
    self.checkButtonAttachmentAvailable.config(state=DISABLED)

  def updateUser(self, *args):
    print(__class__.__name__ + "::" + sys._getframe().f_code.co_name)
    self.announcement.setUser(self.comboBoxUser.get())
    self.scolledText.config(state=NORMAL)
    self.scolledText.delete(1.0, END)
    self.scolledText.insert(INSERT, self.announcement.message.as_string())
    self.scolledText.config(state=DISABLED)
    self.checkAttachments()

  def updateType(self, *args):
    print(__class__.__name__ + "::" + sys._getframe().f_code.co_name)
    self.announcement.setMailType(self.comboBoxType.get())
    self.scolledText.config(state=NORMAL)
    self.scolledText.delete(1.0, END)
    self.scolledText.insert(INSERT, self.announcement.message.as_string())
    self.scolledText.config(state=DISABLED)
    self.checkAttachments()

  def sendTestMail(self):
    print(__class__.__name__ + "::" + sys._getframe().f_code.co_name)
    self.announcement.sendTestMail()

  def sendMail(self):
    print(__class__.__name__ + "::" + sys._getframe().f_code.co_name)
    pwDialog = PasswordDialog(self.frame,
      title=self.announcement.getFullAddressList()[0])
    # print(pwDialog.result)
    if pwDialog.result:
      self.announcement.attach()
      self.announcement.sendMail(pwDialog.result)
      self.announcement.renderMessage()

class Dialog(Toplevel):
  def __init__(self, parent, title = None):
    Toplevel.__init__(self, parent)
    self.transient(parent)
    if title:
      self.title(title)
    self.parent = parent
    self.result = None
    body = Frame(self)
    self.initial_focus = self.body(body)
    body.pack(padx=5, pady=5)
    self.buttonbox()
    self.grab_set()
    if not self.initial_focus:
      self.initial_focus = self
    self.protocol("WM_DELETE_WINDOW", self.cancel)
    self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
      parent.winfo_rooty()+50))
    self.initial_focus.focus_set()
    self.wait_window(self)

  def body(self, master):
    pass # override

  def buttonbox(self):
    box = Frame(self)
    w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
    w.pack(side=LEFT, padx=5, pady=5)
    w = Button(box, text="Cancel", width=10, command=self.cancel)
    w.pack(side=LEFT, padx=5, pady=5)
    self.bind("<Return>", self.ok)
    self.bind("<Escape>", self.cancel)
    box.pack()

  def ok(self, event=None):
    self.withdraw()
    self.update_idletasks()
    self.apply()
    self.cancel()

  def cancel(self, event=None):
    self.parent.focus_set()
    self.destroy()

  def apply(self):
    pass # override

class PasswordDialog(Dialog):
  def body(self, master):
    Label(master, text=self.title()).grid(column=0, row=0, columnspan=2)  
    Label(master, text='Password').grid(column=0, row=1)
    self.entryPassword = Entry(master, show='*')
    self.entryPassword.grid(row=1, column=1, sticky=W)
    return self.entryPassword

  def apply(self):
    self.result = self.entryPassword.get()

class ControlAnnouncementRunner:
  def __init__(self):
    self.startGui()
    
  def startGui(self):
    root = Tk()
    root.title(__class__.__name__ + "::" + sys._getframe().f_code.co_name)
    app = ControlAnnouncement(root)
    root.mainloop()

if '__main__' == __name__:
  ControlAnnouncementRunner()
