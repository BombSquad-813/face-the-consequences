import time
from display import Display

d = Display()
print("Showing ready screen...")
d.show_ready()
time.sleep(5)
print("Showing granted...")
d.show_granted("Haneen")
time.sleep(5)
print("Showing denied...")
d.show_denied("FACE FAIL")
time.sleep(5)
print("Done!")
