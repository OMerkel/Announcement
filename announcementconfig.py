"""Announcement configuration.

The announcement configuration allows to adapt JSON objects for user data
administration, template adaptation, and changing the values to use for
substitutions into the templates, and global common settings for your
scenario.

This file needs adaptation work to match your surrounding environment first.
SMTP and HTML knowledge will be helpful.

MIT licensed, Copyright (c) 2015
@author Oliver Merkel, Merkel(dot)Oliver(at)web(dot)de.
All rights reserved.
"""
mail = {
  "Release Candidate Announcement" : {
    "To" : [ "Releases <releases@your-company.com>" ],
    "CC" : [ "Customer <poc@customer-company.com>", "Project Leader <projectlead@your-company.com>" ],
    "Subject" : "${productversion} ${producttype} - Release Candidate ${calendarmonth} available",
    "Body" : [
      "<html xmlns='http://www.w3.org/TR/REC-html40'><head>",
      "<META HTTP-EQUIV='Content-Type' CONTENT='text/html; charset=iso-8859-1'><style><!--",
      "@font-face {font-family:Arial;panose-1:2 15 5 2 2 2 4 3 2 4;}",
      "p {margin:0cm;margin-bottom:12.0pt;font-size:10.0pt;font-family:'Arial','sans-serif';}",
      "p.signature {margin-left:20.0pt;margin-bottom:8.0pt;font-size:8.0pt;color:black;}",
      "--></style></head>",
      "<body><p>Dear all,</p>",
      "<p>We are near to ${producttype} of ${productversion} again.</p>",
      "<p>Release Candidate of ${productversion} for ${calendarmonth} is available on<br>",
      "<a href='file:///${path}'>${path}</a></p>",
      "${signature}",
      "</body></html>"
    ]
  },
  "Final Delivery Build" : {
    "To" : [ "Releases <releases@your-company.com>" ],
    "CC" : [ "Integration <int@your-company.com>", "Project Leader <projectlead@your-company.com>" ],
    "Subject" : "${productversion} ${producttype} ${calendarmonth} - final delivery build started",
    "Body" : [
      "<html xmlns='http://www.w3.org/TR/REC-html40'><head>",
      "<META HTTP-EQUIV='Content-Type' CONTENT='text/html; charset=iso-8859-1'><style><!--",
      "@font-face {font-family:Arial;panose-1:2 15 5 2 2 2 4 3 2 4;}",
      "p {margin:0cm;margin-bottom:12.0pt;font-size:10.0pt;font-family:'Arial','sans-serif';}",
      "p.signature {margin-left:20.0pt;margin-bottom:8.0pt;font-size:8.0pt;color:black;}",
      "--></style></head>",
      "<body><p>Dear all,</p>",
      "<p>Please note that final delivery build of ${productversion} for ${calendarmonth} has been started on<br>",
      "<a href='${buildserver}'>${buildserver}</a></p>",
      "${signature}",
      "</body></html>"
    ]
  }
}

users = {
  "UserIDorName1" : {
    "Signature" : [
      "<p style='color:#1F497D;margin-bottom:0.1pt'>Kind Regards / Mit freundlichen Gr&uuml;&szlig;en<br>",
      "&nbsp;FirstName1 LastName1</p>",
      "<hr />",
      "<p class=signature><span style='font-size:10.0pt; color:#1F497D'>FirstName1 LastName1, <span style='font-size:8.0pt'>Title</span></span><br>",
      "Position, OU</p>",
      "<p class=signature>Phone: +49 1234 5678 90<br>Fax: +49 1234 5678 09</p>" ],
    "Friendly Name" : "LastName1, FirstName1" ,
    "Mail" : [ "FirstName1.LastName1@your-company.com" ]
  }, "UserIDorName2" : {
    "Signature" : [
      "<p>Best regards, FirstName2 LastName2</p>" ],
    "Friendly Name" : "LastName2, FirstName2",
    "Mail" : [ "FirstName2.LastName2@your-company.com" ]
  }
}

current = { "productversion" : "MyProduct1.1-abc-details",
  "producttype" : "Monthly Release", 
  "calendarmonth" : "15.04",
  "path" : "\\\\someserver\\share\\path1\\path2\\directory",
  "buildserver" : "http://somebuildserver",
  "attachments" : [
    "ReleaseNotes\\Release_Notes.pdf",
    "Testing\\TestReport.pdf",
    "CHANGELOG.txt"
  ]
}

common = { "replymailaddr" : "Release Group <releases@your-company.com>",
  "mailserver" : "mymailserver.your-company.com" }
