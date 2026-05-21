# ============================================================
# gentec_control.py
# Controls Gentec photodiode power meter
# Toggle button starts then stops statistics collection
# Saves full screenshot of Gentec window
# ============================================================

import time
import pyautogui
from config import *


def measure_power_gentec(wavelength, repeat_num, file_prefix, file_num):
    print(f'Gentec measurement at {wavelength} nm repeat {repeat_num}')

    time.sleep(CLICK_WAIT)
    pyautogui.click(x=GENTEC_TASKBAR_X, y=GENTEC_TASKBAR_Y)
    time.sleep(CLICK_WAIT)

    # Type wavelength in input box
    pyautogui.click(x=GENTEC_WAVELENGTH_BOX_X, y=GENTEC_WAVELENGTH_BOX_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.typewrite(str(wavelength), interval=0.1)
    pyautogui.press('enter')
    time.sleep(CLICK_WAIT)

    # Toggle button ON - start statistics
    pyautogui.click(x=GENTEC_STATS_TOGGLE_X, y=GENTEC_STATS_TOGGLE_Y)
    time.sleep(STATS_TIME)

    # Toggle button OFF - stop statistics
    pyautogui.click(x=GENTEC_STATS_TOGGLE_X, y=GENTEC_STATS_TOGGLE_Y)
    time.sleep(1)

    # Save full screenshot
    screenshot = pyautogui.screenshot()
    screenshot_filename = (file_prefix
                          + '_Power'
                          + '_wav_' + str(wavelength) + 'nm'
                          + '_rep_' + str(repeat_num)
                          + '_' + str(file_num)
                          + '.png')
    screenshot.save(screenshot_filename)
    print(f'Gentec screenshot saved: {screenshot_filename}')