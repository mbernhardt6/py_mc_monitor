import smtplib

def sendMail(recipient, sender, subject, message):
  host = "mail.transcendedlife.local"
  
  body = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" % (sender, recipient, subject, message)
  
  smtpObj = smtplib.SMTP(host)
  smtpObj.sendmail(sender, recipient, body)