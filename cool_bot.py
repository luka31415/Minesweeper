import win32api
import time
import win32con
import keyboard

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.02)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

while not keyboard.is_pressed('q'):
    click(188, 178)
    click(188, 348)
    click(101, 262)
    click(101, 430)
    click(271, 262)
    click(271, 430)