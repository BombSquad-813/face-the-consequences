import time
import json
import os

DB = "/home/pi/hackabull/rf_fingerprints.json"

class Sigil:
    def __init__(self):
        self.db = json.load(open(DB)) if os.path.exists(DB) else {}
        print("[RFID] Sigil ready — using keyboard UID input for demo")

    def save(self):
        with open(DB, "w") as f:
            json.dump(self.db, f)

    def enroll(self, name):
        uid = input(f"[RFID] Type card UID to enroll as {name}: ").strip()
        self.db[uid] = {"name": name}
        self.save()
        print(f"[RFID] Enrolled {name} with UID: {uid}")

    def check(self, timeout=15):
        print("[RFID] Tap card (type UID and press Enter):")
        try:
            uid = input().strip()
            if uid in self.db:
                name = self.db[uid]["name"]
                print(f"[RFID] PASS — {name}")
                return True, name, "OK"
            else:
                print(f"[RFID] FAIL — not enrolled")
                return False, None, "NOT ENROLLED"
        except:
            return False, None, "NO INPUT"
