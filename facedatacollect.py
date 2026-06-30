import cv2
import os

# Initialize face detector
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

name = input("Enter person's name: ")
dataset_dir = os.path.join('dataset', name)

if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir)

cap = cv2.VideoCapture(0)
count = 0
collecting = False  # flag to start capturing faces

print("[INFO] Press 's' to start collecting face samples.")
print("[INFO] Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.putText(frame, "Face Detected", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        if collecting:
            count += 1
            face_img = gray[y:y+h, x:x+w]
            file_path = os.path.join(dataset_dir, f"{str(count)}.jpg")
            cv2.imwrite(file_path, face_img)
            cv2.putText(frame, f"Samples: {count}", (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Face Dataset Creator", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        collecting = True
        print("[INFO] Started collecting face samples...")

    elif key == ord('q'):
        print("[INFO] Exiting program...")
        break

    if collecting and count >= 50:
        print(f"[INFO] Dataset collection completed for {name}")
        break

cap.release()
cv2.destroyAllWindows()
