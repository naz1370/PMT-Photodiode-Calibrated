# ============================================================
# motor_control.py
# Controls COSMOS Velmex stepper motor (monochromator)
# ============================================================

import time
import pyautogui
from config import *


def step_motor_up(stepNum):
    print(f'Moving motor up {stepNum} steps')
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=WINDOWS_START_X, y=WINDOWS_START_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=COSMOS_TASKBAR_X, y=COSMOS_TASKBAR_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=COSMOS_MOTOR1_X, y=COSMOS_MOTOR1_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=COSMOS_DISTANCE_BOX_X, y=COSMOS_DISTANCE_BOX_Y)
    pyautogui.click(x=COSMOS_DISTANCE_BOX_X, y=COSMOS_DISTANCE_BOX_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.press('del')
    time.sleep(CLICK_WAIT)
    pyautogui.typewrite(str(stepNum), interval=0.1)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=COSMOS_POSITIVE_X, y=COSMOS_POSITIVE_Y)
    time.sleep(int(float(stepNum) / 2000.) + 1)


def step_motor_down(stepNum):
    print(f'Moving motor down {stepNum} steps')
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=WINDOWS_START_X, y=WINDOWS_START_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=COSMOS_TASKBAR_X, y=COSMOS_TASKBAR_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=COSMOS_MOTOR1_X, y=COSMOS_MOTOR1_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=COSMOS_DISTANCE_BOX_X, y=COSMOS_DISTANCE_BOX_Y)
    pyautogui.click(x=COSMOS_DISTANCE_BOX_X, y=COSMOS_DISTANCE_BOX_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.press('del')
    time.sleep(CLICK_WAIT)
    pyautogui.typewrite(str(stepNum + 100), interval=0.1)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=COSMOS_NEGATIVE_X, y=COSMOS_NEGATIVE_Y)
    time.sleep(int(float(stepNum) / 2000.) + 1)
    # Backlash correction
    pyautogui.click(x=COSMOS_MOTOR1_X, y=COSMOS_MOTOR1_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=COSMOS_DISTANCE_BOX_X, y=COSMOS_DISTANCE_BOX_Y)
    pyautogui.click(x=COSMOS_DISTANCE_BOX_X, y=COSMOS_DISTANCE_BOX_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.press('del')
    time.sleep(CLICK_WAIT)
    pyautogui.typewrite('100', interval=0.1)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=COSMOS_POSITIVE_X, y=COSMOS_POSITIVE_Y)
    time.sleep(1)