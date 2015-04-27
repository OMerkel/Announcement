# Announcement

__Keywords:__ _SMTP, mail announcements, events, Python, tkinter_

Objective of this project is to develop a tool to send mail announcements
using mail templates. The set of templates reflect configured recurring
events to choose from. Typically such events are reasoning any type of
announcement in business life. A group of users is to be configured to
control the Python/tkinter application or a command line version of
the tooling. Placeholders are used in the template and will be
substituted by up-to-date values on demand.

* __controlannouncement.py__ will start the Python/tkinter User Experience.
* __announcement.py__ holds the announcement SMTP based library with a
  simplified command line startup.
* __announcementconfig.py__ will allow to adapt JSON objects for user data
  administration, template adaptation, and changing the values to use for
  substitutions into the templates, and global common settings for your
  scenario.

The usage of this announcement tool intends to minimize copy and paste
errors typical if performed manually. Next the mail announcement gets
a more clear structure compared to manual editing.

MIT licensed, (c) Oliver Merkel
