import numpy as np
import imutils
import time
import cv2
from threading import Thread
import pyttsx3
import os
os.environ['AUDIODEV'] = 'hw:2,0'


# --- Audio setup ---
engine = pyttsx3.init()
engine.setProperty('rate', 125)
engine.setProperty('volume', 1)

engine.say("Object detection")
engine.runAndWait()

def speak_out(texts):
    if texts:
        engine.say("There is " + ", ".join(texts))
        engine.runAndWait()

def audioalert(texts):
    t = Thread(target=speak_out, args=(texts,))
    t.daemon = True
    t.start()

# --- Load YOLO ---
LABELS = open("coco.names").read().strip().split("\n")
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
net = cv2.dnn.readNetFromDarknet("person.cfg", "person.weights")
ln = [net.getLayerNames()[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

# --- Video stream ---
cap = cv2.VideoCapture(0)
time.sleep(2.0)
(W, H) = (None, None)

last_alert_time = 0
alert_interval = 3  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=320)

    if W is None or H is None:
        (H, W) = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (320, 320), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    boxes, confidences, classIDs, centers = [], [], [], []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # Person class in COCO
            if confidence > 0.4:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - width/2)
                y = int(centerY - height/2)

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
                centers.append((centerX, centerY))

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
    texts = []

    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y, w, h) = boxes[i]
            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{LABELS[classIDs[i]]}: {confidences[i]:.2f}", (x, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Determine positions
            cx, cy = centers[i]
            W_pos = "left" if cx < W/3 else "center" if cx < 2*W/3 else "right"
            H_pos = "top" if cy < H/3 else "mid" if cy < 2*H/3 else "bottom"
            texts.append(f"{H_pos} {W_pos} {LABELS[classIDs[i]]}")

    # Trigger audio alert every alert_interval seconds
    if texts and (time.time() - last_alert_time > alert_interval):
        audioalert(texts)
        last_alert_time = time.time()

    #cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
