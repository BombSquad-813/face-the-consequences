import sys
sys.path.insert(0, '/home/pi/.local/lib/python3.13/site-packages')
import threading
import time
import RPi.GPIO as GPIO
from facebreak import FaceBreak
from sigil import Sigil
from display import Display

RELAY_PIN = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH)  # HIGH = locked on boot

disp = Display()
face = FaceBreak()
rfid = Sigil()

def run():
    print("[BOOT] Sentinel Gate online")
    disp.show_ready()

    while True:
        face_res = {"ok": False, "name": None}
        rfid_res = {"ok": False, "name": None}

        def check_face():
            ok, name = face.check(timeout=15)
            face_res["ok"] = ok
            face_res["name"] = name

        def check_rfid():
            ok, name, msg = rfid.check(timeout=15)
            rfid_res["ok"] = ok
            rfid_res["name"] = name
            print(f"[RFID] {msg}")

        t1 = threading.Thread(target=check_face)
        t2 = threading.Thread(target=check_rfid)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        f = face_res["ok"]
        r = rfid_res["ok"]
        name = face_res["name"] or rfid_res["name"] or "Unknown"

        if f and r:
            print(f"[GATE] GRANTED — {name}")
            disp.show_granted(name)
            disp.unlock_door()
        elif r and not f:
            print("[GATE] DENIED — face failed")
            disp.show_denied("FACE FAIL")
            disp.buzz_alert()
        elif f and not r:
            print("[GATE] DENIED — RFID failed")
            disp.show_denied("RFID FAIL")
            disp.buzz_alert()
        else:
            print("[GATE] DENIED — both failed")
            disp.show_denied("BOTH FAIL")
            disp.buzz_alert()

        time.sleep(3)
        disp.show_ready()

if __name__ == "__main__":
    run()
