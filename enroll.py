import os
import sys
import time
from picamera2 import Picamera2
from sigil import Sigil
import face_recognition
import cv2


def enroll_face(name):
    save_dir = "/home/pi/hackabull/known_faces"
    os.makedirs(save_dir, exist_ok=True)

    cam = Picamera2()
    config = cam.create_preview_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
    cam.configure(config)
    cam.start()
    time.sleep(2)

    print(f"[ENROLL] Look at camera — enrolling {name}")

    saved = 0
    start = time.time()

    while saved < 10 and time.time() - start < 25:
        frame = cam.capture_array()
        rgb = frame[:, :, :3]

        # Improve detection reliability
        rgb = cv2.GaussianBlur(rgb, (5, 5), 0)

        # Try HOG first (fast)
        locs = face_recognition.face_locations(rgb, model="hog")

        # Fallback to CNN if nothing found
        if not locs:
            locs = face_recognition.face_locations(rgb, model="cnn")

        if locs:
            path = f"{save_dir}/{name}_{saved}.jpg"
            cv2.imwrite(path, cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
            print(f"[ENROLL] Saved {path}")
            saved += 1
            time.sleep(0.5)
        else:
            print("[ENROLL] No face detected...")

    cam.stop()
    print(f"[ENROLL] Done — {saved} images saved for {name}")


def enroll_badge(name):
    s = Sigil()
    s.enroll(name)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 enroll.py --face haneen")
        print("  python3 enroll.py --face zaid")
        print("  python3 enroll.py --badge haneen")
        sys.exit(1)

    mode = sys.argv[1]
    name = sys.argv[2]

    if mode == "--face":
        enroll_face(name)
    elif mode == "--badge":
        enroll_badge(name) 

