# train_faces.py
import cv2
import os
import numpy as np
from PIL import Image

dataset_path = 'dataset'
recognizer = cv2.face.LBPHFaceRecognizer_create()
faces = []
ids = []
label_dict = {}
current_id = 0

print("[INFO] Training faces...")

for person_name in os.listdir(dataset_path):
    person_dir = os.path.join(dataset_path, person_name)
    if not os.path.isdir(person_dir):
        continue

    label_dict[current_id] = person_name
    for image_name in os.listdir(person_dir):
        image_path = os.path.join(person_dir, image_name)
        img = Image.open(image_path).convert('L')
        img_np = np.array(img, 'uint8')
        faces.append(img_np)
        ids.append(current_id)

    current_id += 1

recognizer.train(faces, np.array(ids))
recognizer.save('trainer.yml')

# Save label names
import pickle
with open('labels.pkl', 'wb') as f:
    pickle.dump(label_dict, f)

print("[INFO] Training complete. Model saved as trainer.yml")
