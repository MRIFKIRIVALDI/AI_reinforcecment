import cv2
from datetime import datetime
import time
import os

os.makedirs("screenshots", exist_ok=True)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

last_seen = time.time()
face_missing_start = None

while True :
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1,minNeighbors=5)

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #1. Deteksi lebih dari satu wajah
    if len(faces) > 1 :
        msg = f"[{now}] Lebih dari satu wajah terdeteksi!"
        print(msg)
        with open("cheating_log.txt", "a") as log:
            log.write(msg + "\n")
        cv2.imwrite(f"screenshots/cheating_{datetime.now().strftime('%H%M%S')}.jpg",frame)

    # 2. Deteksi wajah menghilang
    if len(faces)==0:
        if face_missing_start is None:
            face_missing_start = time.time()
        elif time.time() - face_missing_start > 3:
            msg = f"[{now}] wajah tidak terlihat lebih dari 3 detik"
            print(msg)
            with open("cheating_log.txt", "a") as log:
                log.write(msg + "\n")
            cv2.imwrite(f"screenshots/missing_{datetime.now().strftime('%H%M%S')}.jpg",frame)
            face_missing_start = None

    else:
        face_missing_start = None

    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+x, y+h),(0,225,0),2)
    cv2.putText(frame,f"Detected Faces :{len(faces)}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX,0.8 , (0,255,255),2)
    cv2.imshow("Ujian online - Deteksi Kecurangan",frame)

    #tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()                                    