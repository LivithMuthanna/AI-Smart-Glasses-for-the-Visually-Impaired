import cv2
import easyocr
import os
import RPi.GPIO as GPIO


import pyttsx3
os.environ['AUDIODEV'] = 'hw:2,0'


# --- Audio setup ---
engine = pyttsx3.init()
engine.setProperty('rate', 125)
engine.setProperty('volume', 1)

engine.say("Text reader")
engine.runAndWait()

GPIO.setmode(GPIO.BCM)
BUTTON_STARTREAD = 23
GPIO.setup(BUTTON_STARTREAD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Initialize EasyOCR reader (use English)
reader = easyocr.Reader(['en'])

# Initialize camera (0 = default)
camera = cv2.VideoCapture(0)

print("Press 's' to scan text or 'q' to quit.")

while True:
    ret, frame = camera.read()
    if not ret:
        print("Failed to capture frame")
        break

    cv2.imshow("Text Detection - Press 's' to scan", frame)

    key = cv2.waitKey(1) & 0xFF

    # Press 's' to scan and speak text
    if GPIO.input(BUTTON_STARTREAD) == GPIO.LOW:
        # Save frame temporarily
        cv2.imwrite("frame.jpg", frame)

        # Detect text from the saved image
        results = reader.readtext("frame.jpg")

        detected_text = " ".join([res[1] for res in results])

        if detected_text:
            print("\nDetected Text:\n", detected_text)
            # Use eSpeak to read the text aloud
            os.system(f'espeak "{detected_text}"')
        else:
            print("No text detected.")

    elif key == ord('q'):
        print("Exiting...")
        break

camera.release()
cv2.destroyAllWindows()
