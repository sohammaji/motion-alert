import time
import cv2
from datetime import datetime
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def alert(time, image):
    with open(image, 'rb') as f:
        img = f.read()
    msg = MIMEMultipart()

    msg['subject'] = "Motion Detected!"
    text = MIMEText(f"Some movement has been detected at {time}.")
    msg.attach(text)
    snap = MIMEImage(img, name=os.path.basename(image))
    msg.attach(snap)
    msg['to'] = "sohammaji10@gmail.com"

    user = "johnnyblah69@gmail.com"
    msg['from'] = user
    password = "lwvdfqotmwykjjbd"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()


cap = cv2.VideoCapture(0)
bg = None
prev_movement = datetime.strptime('00:00:00', "%H:%M:%S")
check, frame = cap.read()
time.sleep(2)
while True:
    check, frame = cap.read()

    # Performing morphological operations to remove noise
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (21, 21), 0)

    if bg is None:
        bg = blur
        continue

    # Background subtraction method
    delta_frame = cv2.absdiff(bg, blur)
    # thres = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    delta_frame = cv2.erode(delta_frame, None, iterations=3)
    delta_frame = cv2.dilate(delta_frame, None, iterations=3)
    delta_frame = cv2.GaussianBlur(delta_frame, (21, 21), 0)
    thres = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    # Finding contours
    (cntr, _) = cv2.findContours(thres.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cntr:
        if cv2.contourArea(contour)<10000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "MOVEMENT DETECTED", (170, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Sending the alert via email(1 mail per 5 minutes)
        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')
        diff = (now - prev_movement)
        diff = diff.seconds
        if diff > 300:
            cv2.imwrite("snapshot.png", frame)
            alert(dtString, "snapshot.png")
            prev_movement = datetime.strptime(dtString, "%H:%M:%S")

    cv2.imshow("Webcam", frame)
    cv2.imshow("thres", cv2.resize(thres, (400, 300)))
    cv2.imshow("delta", cv2.resize(delta_frame, (400, 300)))
    cv2.imshow("blur", cv2.resize(blur, (400, 300)))

    key = cv2.waitKey(1)
    if key == ord('q' or 'Q'):
        break

cap.release()
cv2.destroyAllWindows()

