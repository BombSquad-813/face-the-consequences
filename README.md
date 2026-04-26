# 🔐 face-the-consequences

> *"Every badge can be cloned. Every face can be printed. We fixed both."*

**Sentinel Gate** — a dual-factor physical access control system built in 24 hours at **Hackabull 2025**, University of South Florida.

---

## 🎯 What It Does

Most door systems use ONE security check. We use TWO — simultaneously. Both must pass or the door stays locked.

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   FACTOR 1 — FaceBreak        FACTOR 2 — Sigil     │
│   ─────────────────────        ────────────────     │
│   Pi Camera detects your       RFID reader checks   │
│   face + verifies you're       your badge ID is     │
│   actually alive (blink)       enrolled             │
│                                                     │
│              ↓           AND          ↓             │
│                                                     │
│         ┌─────────────────────────┐                 │
│         │   Master Controller     │                 │
│         │   (AND Gate Logic)      │                 │
│         └──────────┬──────────────┘                 │
│                    ↓                                │
│         PASS → Solenoid UNLOCKS 🔓                  │
│         FAIL → Red LED + Buzzer 🚨                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🛡️ Attack Scenarios We Block

| Attack | What Happens |
|--------|-------------|
| 📸 Printed photo of your face | **DENIED** — no blink detected |
| 📱 Screen replay attack | **DENIED** — screen flicker at 60Hz caught |
| 🪪 Stolen badge, no face | **DENIED** — face factor fails |
| ⚡ Cloned badge + real face | **DENIED** — badge not enrolled |
| 💀 Photo + cloned badge | **DENIED** — both factors fail |
| ✅ Real face + enrolled badge | **GRANTED** — solenoid clicks open |

---

## 🔧 Hardware Stack

```
Raspberry Pi 4 (2GB)
├── Arducam 8MP IMX219 Camera  →  Face detection + liveness
├── SSD1306 OLED 128x64        →  Status display
├── HiLetgo 5V Relay Module    →  Solenoid control
├── 12V Solenoid Lock          →  Physical door mechanism
├── WS2812B NeoPixel Ring      →  Green breathe / Red strobe
├── Passive Buzzer             →  Audio alert on deny
└── PN532 RFID Module          →  Badge authentication
```

---

## 💻 Software Stack

```
Python 3.13 on Raspberry Pi OS (64-bit)
├── picamera2          →  Camera capture
├── face_recognition   →  Face encoding + identity match
├── OpenCV             →  Image processing + EAR blink detection
├── luma.oled          →  OLED display control
├── RPi.GPIO           →  Relay + LED + buzzer GPIO
└── rpi_ws281x         →  NeoPixel LED ring
```

---

## 📁 Project Structure

```
face-the-consequences/
├── main.py          # AND gate master controller
├── facebreak.py     # FaceBreak — liveness + identity
├── sigil.py         # Sigil — RFID badge authentication  
├── display.py       # OLED + NeoPixel + buzzer + relay
├── enroll.py        # Enrollment script for faces + badges
└── known_faces/     # Enrolled face images (gitignored)
```

---

## 🚀 How It Works

### Factor 1 — FaceBreak (Liveness Detection)

Uses **Eye Aspect Ratio (EAR)** to detect real blinks:

```python
def eye_aspect_ratio(self, eye):
    A = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))
    B = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))
    C = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))
    return (A + B) / (2.0 * C)
    # EAR < 0.22 = blink detected
    # Photo = 0 blinks = DENIED
```

### Factor 2 — Sigil (Badge Authentication)

Reads badge UID and cross-references enrolled database:

```python
def check(self, timeout=15):
    uid = self.read_uid()
    if uid not in self.db:
        return False, None, "NOT ENROLLED"
    return True, self.db[uid]["name"], "OK"
```

### AND Gate Logic

```python
if face_ok and rfid_ok:
    disp.show_granted(name)
    disp.unlock_door()      # GPIO 17 LOW → relay fires
else:
    disp.show_denied(reason)
    disp.buzz_alert()       # 2kHz PWM buzz
```

---

## ⚡ Quick Start

```bash
# Clone the repo
git clone https://github.com/BombSquad-813/face-the-consequences.git
cd face-the-consequences

# Install dependencies on Raspberry Pi
pip3 install face_recognition picamera2 luma.oled rpi_ws281x --break-system-packages

# Enroll your face
python3 enroll.py --face yourname

# Enroll your badge
python3 enroll.py --badge yourname

# Run the system
sudo python3 main.py
```

---

## 📍 Wiring Reference

| Component | Pi Pin | GPIO |
|-----------|--------|------|
| OLED VCC | Pin 1 | 3.3V |
| OLED GND | Pin 6 | GND |
| OLED SDA | Pin 3 | GPIO 2 |
| OLED SCL | Pin 5 | GPIO 3 |
| Relay IN | Pin 11 | GPIO 17 |
| NeoPixel DIN | Pin 12 | GPIO 18 |
| Buzzer + | Pin 32 | GPIO 12 |

---

## 👥 Team

Built in 24 hours at **Hackabull 2025** — USF Hardware Track

| Name | Role |
|------|------|
| Haneen | Hardware Lead + System Integration |
| Khaled | RFID Hardware + NeoPixel + Relay |
| Deema | Software Lead + Face Recognition |
| Anna | Testing + Demo + Documentation |

---

## 🏆 Built At

**Hackabull 2025** · University of South Florida · Hardware Track

*No cloud. No app. No compromise. Just a Pi, a camera, and consequences.*

---

## ⚠️ Security Note

Face images and badge fingerprint data are excluded from this repository via `.gitignore` to protect enrolled users' biometric data.
