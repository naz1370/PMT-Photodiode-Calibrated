# ============================================================
# pd_control.py
# Controls photodiode position via PuTTY serial terminal
# 'i' moves PD into beam path for power reference measurement
# 'o' moves PD out of beam path for PMT measurement
# PuTTY must be open and maximized before running main.py
# ============================================================

import time
import pyautogui
from config import *


def move_pd(direction):
    if direction == 'i':
        print('Moving PD INTO beam path')
    elif direction == 'o':
        print('Moving PD OUT of beam path')
    else:
        print(f'Unknown direction: {direction}')
        return

    time.sleep(CLICK_WAIT)
    pyautogui.click(x=PUTTY_X, y=PUTTY_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.typewrite(direction, interval=0.1)
    pyautogui.press('enter')
    time.sleep(PD_MOVE_TIME)
    print('PD move complete')