import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import win32gui
from plyer import notification

# Volume threshold
VOLUME_THRESHOLD = 0.70  # 70%
SAFE_VOLUME = 0.10       # 

# Get volume interface
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_interface = cast(interface, POINTER(IAudioEndpointVolume))

def get_current_volume():
    return volume_interface.GetMasterVolumeLevelScalar()

def set_volume(level):
    volume_interface.SetMasterVolumeLevelScalar(level, None)

def get_active_window_title():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

last_window = ""

while True:
    try:
        current_window = get_active_window_title()

        if current_window != last_window:
            vol = get_current_volume()
            if vol > VOLUME_THRESHOLD:
                set_volume(SAFE_VOLUME)
                print(f"[!] Volume was high ({vol*100:.0f}%). Lowered to {SAFE_VOLUME*100:.0f}%")
                notification.notify(
                    title="Volume Adjusted",
                    message=f"Switched to {current_window}. Volume lowered to safe level.",
                    timeout=3
                )
            last_window = current_window

        time.sleep(1)
    except KeyboardInterrupt:
        print("Exited by user.")
        break
