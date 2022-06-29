import cv2
import datetime
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
while True:
    _, frame = cap.read()
    original_frame = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, 1.3, 5)
    for x, y, w, h in face:
        img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
        # face_roi = frame[y:y+h, x:x+w]
        # gray_roi = gray[y:y+h, x:x+w]
        time_stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        file_name = f'photos\\img-{time_stamp}.png'
        cv2.imwrite(file_name, original_frame)        
    cv2.imshow('CAMERA', frame)
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break