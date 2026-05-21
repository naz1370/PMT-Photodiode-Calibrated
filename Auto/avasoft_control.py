# ============================================================
# avasoft_control.py
# Controls AVASoft spectrometer
# Saves absolute intensity as ASCII file
# ============================================================

import time
import pyautogui
from config import *


def save_intensity_with_avasoft(file_prefix, file_num, rep):
    print(f'Saving AVASoft intensity: {file_prefix}_rep_{rep}_{file_num}')
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=WINDOWS_START_X, y=WINDOWS_START_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=AVASOFT_TASKBAR_X, y=AVASOFT_TASKBAR_Y)
    time.sleep(1)
    pyautogui.click(x=AVASOFT_HOME_X, y=AVASOFT_HOME_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=AVASOFT_ABS_INTENSITY_X, y=AVASOFT_ABS_INTENSITY_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=AVASOFT_START_X, y=AVASOFT_START_Y)
    time.sleep(INTEGRATION_TIME)
    time.sleep(CLICK_WAIT)
    pyautogui.press('enter')
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=AVASOFT_FILE_X, y=AVASOFT_FILE_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=AVASOFT_EXPORT_X, y=AVASOFT_EXPORT_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=AVASOFT_ASCII_X, y=AVASOFT_ASCII_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.press('enter')
    time.sleep(1)
    filename = file_prefix + '_Inten_dial_' + str(file_num) + '_rep_' + str(rep)
    pyautogui.typewrite(filename, interval=0.1)
    time.sleep(CLICK_WAIT)
    pyautogui.press('enter')
    time.sleep(5)
    print(f'AVASoft file saved: {filename}')
