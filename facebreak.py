import sys
sys.path.insert(0, '/home/pi/.local/lib/python3.13/site-packages')
import face_recognition
import numpy as np
import os
import time
from picamera2 import Picamera2

class FaceBreak:
    def __init__(self, known_dir="/home/pi/hackabull/known_faces"):
        self.known_encodings = []
        self.known_names = []
        self.blink_count = 0
        self.last_eye_state = "open"
        self.cam = Picamera2()
        config = self.cam.create_still_configuration(main={"size": (640, 480)})
        self.cam.configure(config)
        self.cam.start()
        time.sleep(2)
        self.load_known_faces(known_dir)

    def load_known_faces(self, directory):
        print("[FACE] Loading known faces...")
        for f in os.listdir(directory):
            if f.endswith((".jpg", ".png")):
                path = os.path.join(directory, f)
                img = face_recognition.load_image_file(path)
                enc = face_recognition.face_encodings(img)
                if enc:
                    self.known_encodings.append(enc[0])
                    self.known_names.append(f.split("_")[0])
        print(f"[FACE] {len(self.known_encodings)} faces loaded")

    def eye_aspect_ratio(self, eye):
        A = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))
        B = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))
        C = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))
        return (A + B) / (2.0 * C)

    def check(self, timeout=15):
        self.blink_count = 0
        self.last_eye_state = "open"
        start = time.time()
        while time.time() - start < timeout:
            frame = self.cam.capture_array()
            rgb = frame[:, :, :3]
            locs = face_recognition.face_locations(rgb)
            if not locs:
                continue
            marks = face_recognition.face_landmarks(rgb, locs)
            if marks:
                left = marks[0].get("left_eye", [])
                if len(left) == 6:
                    ear = self.eye_aspect_ratio(left)
                    if ear < 0.22:
                        if self.last_eye_state == "open":
                            self.blink_count += 1
                            print(f"[FACE] Blink #{self.blink_count}")
                        self.last_eye_state = "closed"
                    else:
                        self.last_eye_state = "open"
            if self.blink_count < 1:
                continue
            encs = face_recognition.face_encodings(rgb, locs)
            if not encs:
                continue
            matches = face_recognition.compare_faces(
                self.known_encodings, encs[0], tolerance=0.6)
            if any(matches):
                name = self.known_names[matches.index(True)]
                print(f"[FACE] PASS - {name}")
                return True, name
        print("[FACE] FAIL")
        return False, None
