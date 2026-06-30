#!/usr/bin/env python3
import lgpio
import subprocess, time, os, signal, sys, atexit
import pyttsx3
import os
os.environ['AUDIODEV'] = 'hw:2,0'

# Wait for system boot
#time.sleep(5)
engine = pyttsx3.init()
engine.setProperty('rate', 125)
engine.setProperty('volume', 1)

engine.say("Ready to run")
engine.runAndWait()
# Pin numbers (BCM)
BUTTON_OBJECT = 17
BUTTON_FACE = 27
BUTTON_READING = 22

chip = None
for attempt in range(5):  # retry 5 times
    try:
        chip = lgpio.gpiochip_open(0)
        for pin in [17, 27, 22]:
            lgpio.gpio_claim_input(chip, pin, lgpio.SET_PULL_UP)
        print("GPIO setup successful!")
        break
    except lgpio.error as e:
        print(f"Attempt {attempt+1}: GPIO busy, retrying in 2s...")
        time.sleep(2)
else:
    print("Failed to claim GPIO after retries. Exiting.")
    sys.exit(1)

def cleanup():
    print("Cleaning up...")
    for pin in [BUTTON_OBJECT, BUTTON_FACE, BUTTON_READING]:
        try:
            lgpio.gpio_free(chip, pin)
        except Exception:
            pass
    lgpio.gpiochip_close(chip)

atexit.register(cleanup)

# Process management
current_process = None

def stop_current_process():
    global current_process
    if current_process:
        try:
            os.killpg(os.getpgid(current_process.pid), signal.SIGTERM)
        except Exception:
            pass
        current_process = None

def run_script(script_name):
    global current_process
    stop_current_process()
    print(f"Starting {script_name}")
    current_process = subprocess.Popen(
        ["python3", script_name],
        preexec_fn=os.setsid,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

# Main loop
last_state = {BUTTON_OBJECT: 1, BUTTON_FACE: 1, BUTTON_READING: 1}

try:
    while True:
        for pin, script in [
            (BUTTON_OBJECT, "objectdetection.py"),
            (BUTTON_FACE, "facedetection.py"),
            (BUTTON_READING, "bookreadingocr.py")
        ]:
            state = lgpio.gpio_read(chip, pin)
            if state == 0 and last_state[pin] == 1:
                print(f"Button {pin} pressed ? Running {script}")
                run_script(script)
            last_state[pin] = state
        time.sleep(0.1)

except KeyboardInterrupt:
    cleanup()
    sys.exit(0)
