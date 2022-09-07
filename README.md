# Motion Alert [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
#### This is an conceptual security system which detects any movement and notifies the user.
#### This project is made using Python OpenCV module.

---
### Pre-requirements
I ahve used 5 python modules in this code : OpenCV, smtplib, os, datetime and email.mime(MIMEText, MIMEImage, MIMEMultipart). Make sure those modules are installed on your system.

---
### How to use
 1. Just copy the python code and run it on your system.
 2. Replace the email at line 20 with your own email address.
 3. You can use your own SMTP server using your second email address.
 
---
### How it works
Whenever any motion is detected on the camera an alert mail is sent to the email address with an snapshot of the movement. If the movement continues to happen a mail is sent every 5 minutes attached with a snapshot.

---
#### Feel free to suggest for any improvement.
## Thank You.
