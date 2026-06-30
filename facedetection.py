# face_recognition_live.py
import cv2
import pickle
import pyttsx3
import time
import os
os.environ['AUDIODEV'] = 'hw:2,0'

engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.say("Face recognition")
engine.runAndWait()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

with open('labels.pkl', 'rb') as f:
    labels = pickle.load(f)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
engine.say("facedetection activated")
cam = cv2.VideoCapture(0)

last_name = ""
last_time = 0

print("[INFO] Starting face recognition...")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        id_, conf = recognizer.predict(gray[y:y+h, x:x+w])

        if conf > 20:
            name = labels[id_]
        else:
            name = "Unknown"

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"{name} ({int(conf)})", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Announce voice every 5 seconds or for new face
        if name != last_name or time.time() - last_time > 5:
            engine.say(f"{name} detected")
            engine.runAndWait()
            last_name = name
            last_time = time.time()

    #cv2.imshow('Face Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
