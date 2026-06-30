# 👓 AI Smart Glasses for the Blind

An AI-powered, offline assistive wearable that helps visually impaired individuals perceive their surroundings through **real-time object detection, face recognition, and text-to-speech reading** — built entirely on a **Raspberry Pi 5**.

![Working Model](images/working_model.png)

---

## 📌 Overview

Millions of visually impaired individuals struggle with everyday tasks like identifying objects, recognizing people, and reading printed text. Existing assistive devices are often expensive, cloud-dependent, or limited to a single function.

This project presents a **compact, low-cost, fully offline AI assistive device** that combines three core capabilities into a single GPIO-button-controlled system:

- 🟢 **Object Detection** — Identifies objects in the environment and gives directional audio cues (e.g., *"person on left"*, *"chair on right"*) using **YOLOv3**.
- 🟢 **Face Recognition** — Recognizes known individuals from a trained dataset using the **LBPH (Local Binary Pattern Histogram)** algorithm and announces their name.
- 🟢 **Text Reading (OCR)** — Reads printed text from books, signboards, and documents aloud using **EasyOCR / Tesseract** + **pyttsx3** text-to-speech.

All processing runs **locally on-device** — no internet connection or cloud dependency required, ensuring low latency and full user privacy.

> 🎓 Final Year B.E. Project — Department of Artificial Intelligence & Data Science, Coorg Institute of Technology (VTU, Belagavi) — 2025–2026

---

## 🎯 Objectives

- Develop an AI-powered assistive system using Raspberry Pi 5 for visually impaired individuals.
- Implement real-time object detection using YOLO for identifying objects in the user's surroundings.
- Integrate face recognition using the LBPH algorithm for identifying known individuals.
- Build a text-reading module using EasyOCR and pyttsx3 for extraction and speech synthesis.
- Automate startup via `systemd` and enable hands-free control through GPIO push buttons.
- Deliver clear, private audio output via a USB audio converter and earphones.
- Provide a cost-effective, compact, energy-efficient embedded AI solution.

---

## 🏗️ System Architecture

The system runs autonomously on boot via a `systemd` service. A GPIO-based 4-button interface lets the user trigger object detection, face recognition, text reading, or image capture without needing a screen.

```
USB Camera ──► Raspberry Pi 5 ──► AI/OCR Processing ──► Python Scripts ──► USB Audio Converter ──► Earphones
                     ▲
              GPIO Push Buttons
        (Object Detection | Face Recognition | Text Reading | Image Capture)
```

**Control Flow:**

| Button | Function |
|--------|----------|
| KEY 1 | Object Detection (YOLOv3) |
| KEY 2 | Face Recognition (LBPH) |
| KEY 3 | Trigger OCR on captured image |
| KEY 4 | Capture image for text reading |

---

## 🔩 Hardware Components

| Component | Description |
|---|---|
| **Raspberry Pi 5** | Quad-core ARM Cortex-A76 (Broadcom BCM2712) @ ~2.4 GHz, up to 16 GB LPDDR4X RAM, Wi-Fi/Bluetooth, USB-C power — the central processing unit of the system. |
| **USB Camera (Zebronics)** | Captures real-time video/images used for object detection, face recognition, and OCR. |
| **Push Buttons (4-Key Module)** | Wired to GPIO pins; provides a screen-free tactile interface to select functions. |
| **USB Audio Converter** | Routes clean digital-to-analog audio output to earphones via a 3.5 mm jack. |
| **Earphones** | Delivers private, real-time spoken feedback to the user. |
| **Power Supply (5V, 3A)** | Stable power source for the Raspberry Pi and all peripherals. |
| **MicroSD Card (32 GB+)** | Stores the OS, trained models (YOLO, LBPH face dataset), and project code. |

<table>
<tr>
<td align="center"><img src="images/raspberry_pi5.png" width="380"/><br/><b>Raspberry Pi 5</b></td>
<td align="center"><img src="images/usb_camera.png" width="220"/><br/><b>USB Camera (Zebronics)</b></td>
</tr>
<tr>
<td align="center"><img src="images/push_buttons.png" width="300"/><br/><b>4-Key Push Button Module</b></td>
<td align="center"><img src="images/usb_audio_converter.png" width="300"/><br/><b>USB Audio Converter</b></td>
</tr>
</table>

---

## 💻 Software & Technologies Used

| Technology | Role in the Project |
|---|---|
| **Python 3.11** | Core language tying together hardware control, AI inference, and audio output. |
| **Raspberry Pi OS (Bookworm/Bullseye)** | Lightweight Debian-based OS managing hardware resources and `systemd` services. |
| **OpenCV** | Image preprocessing, Haar Cascade face detection, and LBPH face recognition. |
| **YOLOv3** | Real-time object detection model — predicts bounding boxes & class probabilities in a single pass. |
| **EasyOCR / Tesseract OCR** | Extracts printed/handwritten text from captured images. |
| **pyttsx3** | Fully offline text-to-speech engine for audio feedback (no internet dependency). |
| **NumPy** | Efficient numerical handling of image arrays during processing. |
| **Pandas** | Manages structured data such as face-ID datasets and detection logs. |
| **RPi.GPIO** | Reads push-button states from GPIO pins for mode selection. |
| **systemd** | Automatically launches the main script on boot for hands-free, reliable operation. |

---

## ⚙️ Module Breakdown

### 1. Object Detection (YOLOv3)
Detects multiple objects (person, chair, bottle, etc.) in the camera frame and provides **directional audio feedback** based on the object's spatial position, using Intersection-over-Union (IoU) for accurate localization.

### 2. Face Recognition (OpenCV + LBPH)
Trained on a custom face dataset; detects faces via Haar Cascades and recognizes them via LBPH, announcing the matched person's name through speech.

### 3. Text Reading (EasyOCR / Tesseract + pyttsx3)
Captures an image of a document or sign, extracts text via OCR, and reads it aloud — enabling users to "hear" books, labels, and signboards.

### 4. Control Module (GPIO Buttons)
Debounced, pull-up configured GPIO buttons map directly to each function, providing a fully screen-free, hands-free interface.

---

## 📊 Results

| Operation | Metric Used | Accuracy |
|---|---|---|
| Object Detection | IoU / mAP | **72.31%** |
| Face Recognition | (TP+TN)/(TP+TN+FP+FN) | **72.5%** |
| Text Reading | Character Accuracy Rate (CAR) | **83.2%** |

The system delivered near real-time performance with minimal latency, stable thermal behavior, and reliable offline operation throughout testing.

### Output Samples

<table>
<tr>
<td align="center"><img src="images/text_reading_output.png" width="420"/><br/><b>Text Reading (OCR) Output</b></td>
<td align="center"><img src="images/face_recognition_output.png" width="420"/><br/><b>Face Recognition Output</b></td>
</tr>
</table>

---

## ⚖️ Comparison with Existing Systems

| System | Technology | Limitation | Our Advantage |
|---|---|---|---|
| Ultrasonic Smart Cane | Ultrasonic Sensor | Cannot identify objects or read text | Multi-object detection + audio feedback |
| Third Eye for the Blind (ESP32-CAM) | TensorFlow Lite | Limited processing speed/accuracy | YOLOv3 on Raspberry Pi for faster real-time detection |
| Smart Glass using Pi Zero 2W | Vision Language Models | High latency, limited local storage | Fully offline, faster feedback |
| **Proposed System** | **YOLOv3 + OCR + Pyttsx3** | Minor accuracy drop in low light | Unified, low-cost, compact, fully offline solution |

---

## ⚠️ Limitations

- **Lighting Sensitivity** — Detection/OCR accuracy drops in dim or uneven lighting.
- **Noisy Environments** — Audio feedback can be harder to hear outdoors or in crowds.
- **Handwritten Text** — Lower accuracy on cursive/complex handwriting.
- **Battery Life** — ~3.5 hours of continuous use.
- **Thermal Load** — Continuous inference increases CPU temperature.

---

## 🚀 Future Enhancements

- 🗺️ GPS & navigation integration (Google Maps API) for route guidance and emergency tracking.
- ☁️ Cloud connectivity for model updates and secure data backup.
- 🔧 Custom PCB design for a smaller, lighter wearable form factor.
- 🔋 Improved battery management with low-power AI chips / solar charging.
- 🎙️ Gesture and voice command control.
- 🌐 Multi-language support, especially for regional Indian languages.
- 🧠 Continual learning from user data for personalized recognition.

---

## 🧠 Skills Demonstrated

`Computer Vision` · `Embedded AI` · `Raspberry Pi` · `YOLOv3` · `OpenCV` · `OCR` · `Text-to-Speech` · `GPIO Programming` · `Python` · `Assistive Technology` · `systemd Automation`

---

## 👥 Project Team

| Name | USN |
|---|---|
| Kaveramma Inchara T D | 4CI22AD015 |
| **Livith Muthanna M A** | 4CI22AD019 |
| Myla Accamma T B | 4CI22AD023 |
| Nikhil Madappa D G | 4CI22AD027 |

**Guide:** Mr. Ramesh H R, HOD, Dept. of Artificial Intelligence & Data Science
**Institution:** Coorg Institute of Technology, Ponnampet (Affiliated to VTU, Belagavi)

---

## 📚 References

1. [Smart Glasses for Blind People Using Obstacle Detection — IEEE 2023](https://ieeexplore.ieee.org/document/9648186)
2. [Third Eye for the Blind — GitHub](https://github.com/Bhavitejareddy/Third-Eye-For-The-Blind)
3. Redmon, J., & Farhadi, A. (2018). *YOLOv3: An Incremental Improvement.* arXiv:1804.02767.
4. [OpenCV Documentation](https://docs.opencv.org)
5. [EasyOCR Documentation](https://www.jaided.ai/easyocr)
6. [pyttsx3 Documentation](https://pyttsx3.readthedocs.io)
7. [Raspberry Pi 5 Technical Specifications](https://www.raspberrypi.com)
8. [systemd Documentation](https://www.freedesktop.org/wiki/Software/systemd)
9. [GPIO Zero Documentation](https://gpiozero.readthedocs.io)

---

## 📄 License

This project was developed for academic purposes as part of the B.E. curriculum at Coorg Institute of Technology (VTU). Feel free to fork and build upon it for educational or non-commercial use.

---

⭐ If you find this project useful or interesting, consider giving it a star!
