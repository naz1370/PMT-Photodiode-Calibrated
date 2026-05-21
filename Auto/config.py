# ============================================================
# config.py
# Photocathode Sensitivity Automation
# University of Manitoba - MOLLER Experiment
# Updated: 4 May 2026 (post system update)
# ============================================================

# --- Scan Settings ---
DIAL_START = 467
DIAL_END = 850
DIAL_INTERVAL = 20
STEPS_PER_DIAL = 4360

WAVELENGTH_START = 230
WAVELENGTH_END = 510
WAVELENGTH_INTERVAL = 20

# --- Repeat Settings ---
NUM_REPEATS = 5

# --- Timing ---
INTEGRATION_TIME = 6    # seconds - AVASoft intensity measurement
STATS_TIME = 5           # seconds - Gentec statistics collection
PD_MOVE_TIME = 10         # seconds - wait for PD to move in/out
CLICK_WAIT = 0.5          # seconds - between pyautogui clicks

# --- Windows Start Bar ---
WINDOWS_START_X = 19
WINDOWS_START_Y = 1003

# --- COSMOS Motor Coordinates ---
COSMOS_TASKBAR_X = 662
COSMOS_TASKBAR_Y = 1010
COSMOS_MOTOR1_X = 239
COSMOS_MOTOR1_Y = 166
COSMOS_DISTANCE_BOX_X = 369
COSMOS_DISTANCE_BOX_Y = 146
COSMOS_POSITIVE_X = 406
COSMOS_POSITIVE_Y = 197
COSMOS_NEGATIVE_X = 322
COSMOS_NEGATIVE_Y = 201

# --- AVASoft Coordinates ---
AVASOFT_TASKBAR_X = 842
AVASOFT_TASKBAR_Y = 1005
AVASOFT_HOME_X = 280
AVASOFT_HOME_Y = 172
AVASOFT_ABS_INTENSITY_X = 491
AVASOFT_ABS_INTENSITY_Y = 230
AVASOFT_START_X = 23
AVASOFT_START_Y = 83
AVASOFT_FILE_X = 331
AVASOFT_FILE_Y = 174
AVASOFT_EXPORT_X = 452
AVASOFT_EXPORT_Y = 216
AVASOFT_ASCII_X = 478
AVASOFT_ASCII_Y = 257

# --- Gentec Coordinates ---
GENTEC_TASKBAR_X = 743
GENTEC_TASKBAR_Y = 1008
GENTEC_WAVELENGTH_BOX_X = 1011
GENTEC_WAVELENGTH_BOX_Y = 243
GENTEC_STATS_TOGGLE_X = 589
GENTEC_STATS_TOGGLE_Y = 192

# --- PuTTY Coordinates ---
PUTTY_X = 798
PUTTY_Y = 1001

# --- Keithley Coordinates ---
KEITHLEY_TASKBAR_X = 708
KEITHLEY_TASKBAR_Y = 1009
KEITHLEY_COMMAND_BOX_X = 194
KEITHLEY_COMMAND_BOX_Y = 929
KEITHLEY_RUN_SCRIPT_X = 168
KEITHLEY_RUN_SCRIPT_Y = 54
