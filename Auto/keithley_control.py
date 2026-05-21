# ============================================================
# keithley_control.py
# Controls Keithley Communicator
# Scripts: C:\Users\Amilia\Desktop\KeithleyScriptsApril3\
#
# Sequence:
#   Initialize once at start of scan
#   Per wavelength per repeat:
#       TakeData-2Times.txt → wait 10s
#       ReadData.txt        → read and save output
# ============================================================

import time
import pyautogui
import pyperclip
from config import *

KEITHLEY_SCRIPTS = r'C:\Users\Amilia\Desktop\KeithleyScriptsApril3'


def keithleyCom():
    pyautogui.click(x=WINDOWS_START_X, y=WINDOWS_START_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=KEITHLEY_TASKBAR_X, y=KEITHLEY_TASKBAR_Y)


def clearHistory():
    pyautogui.click(x=WINDOWS_START_X, y=WINDOWS_START_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=KEITHLEY_TASKBAR_X, y=KEITHLEY_TASKBAR_Y)
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=56, y=34)
    pyautogui.click(x=113, y=321)
    pyautogui.click(x=56, y=34)
    pyautogui.click(x=100, y=127)


def run_Script(file_path):
    pyautogui.hotkey('winleft', 'r')
    pyautogui.write('notepad')
    pyautogui.press('enter')
    time.sleep(0.1)
    pyautogui.hotkey('alt', 'f')
    pyautogui.press('o')
    pyautogui.write(file_path)
    pyautogui.press('enter')
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.hotkey('alt', 'f4')
    time.sleep(CLICK_WAIT)
    clearHistory()
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=KEITHLEY_COMMAND_BOX_X, y=KEITHLEY_COMMAND_BOX_Y)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(CLICK_WAIT)
    pyautogui.click(x=KEITHLEY_RUN_SCRIPT_X, y=KEITHLEY_RUN_SCRIPT_Y)


def getOutput():
    clearHistory()
    pyautogui.press('f2')
    time.sleep(2)
    pyautogui.moveTo(x=24, y=81)
    time.sleep(2)
    pyautogui.mouseDown()
    time.sleep(2)
    pyautogui.moveTo(x=1268, y=730, duration=1)
    time.sleep(2)
    pyautogui.mouseUp()
    pyautogui.hotkey('ctrl', 'c')
    return pyperclip.paste()


def initialize_keithley():
    print('Initializing Keithley...')
    run_Script(KEITHLEY_SCRIPTS + r'\Intialize.txt')
    time.sleep(2)
    print('Keithley initialized')


def measure_keithley(wavelength, repeat_num, file_prefix):
    print(f'Keithley measurement at {wavelength} nm repeat {repeat_num}')

    # Take 2 data points
    run_Script(KEITHLEY_SCRIPTS + r'\TakeData-2Times.txt')
    time.sleep(10)

    # Read the data
    run_Script(KEITHLEY_SCRIPTS + r'\ReadData.txt')
    measurement = getOutput()

    # Append to text file
    keithley_filename = file_prefix + '_Keithley.txt'
    with open(keithley_filename, 'a') as f:
        f.write(f'wavelength={wavelength}nm, '
                f'repeat={repeat_num}, '
                f'data={measurement}\n')

    print(f'Keithley data saved: {keithley_filename}')
