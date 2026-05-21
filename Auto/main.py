# ============================================================
# main.py
# Photocathode Sensitivity Automation
# University of Manitoba - MOLLER Experiment
#
# Sequence per wavelength per repeat:
#   PD IN  → Gentec screenshot (power reference)
#   PD OUT → Keithley measurement (PMT current)
#   PD OUT → AVASoft intensity → save ASCII (PMT spectrum)
# Move motor to next wavelength
# ============================================================

import time
from motor_control import step_motor_up, step_motor_down
from avasoft_control import save_intensity_with_avasoft
from gentec_control import measure_power_gentec
from pd_control import move_pd
from keithley_control import measure_keithley, initialize_keithley
from config import *


def get_user_inputs():
    print('=' * 55)
    print('   Photocathode Sensitivity Automation')
    print('   University of Manitoba - MOLLER Experiment')
    print('=' * 55)
    serial_number = input('Enter PMT serial number: ')
    date = input('Enter date (DDMMYYYY): ')
    file_prefix = f'PMT-{serial_number}-{date}'

    total_wavelengths = (
        (WAVELENGTH_END - WAVELENGTH_START) // WAVELENGTH_INTERVAL + 1
    )

    print(f'\nFile prefix:        {file_prefix}')
    print(f'Wavelength range:   {WAVELENGTH_START} to {WAVELENGTH_END} nm')
    print(f'Wavelength steps:   {total_wavelengths}')
    print(f'Repeats per step:   {NUM_REPEATS}')
    print(f'Gentec screenshots: {total_wavelengths * NUM_REPEATS}')
    print(f'Keithley readings:  {total_wavelengths * NUM_REPEATS}')
    print(f'AVASoft files:      {total_wavelengths * NUM_REPEATS}')

    input('\nMake sure all software is open. '
          'Press Enter to start or Ctrl+C to cancel...')
    return file_prefix


def run_scan(file_prefix):
    dial = DIAL_START
    wavelength = WAVELENGTH_START
    step = int(STEPS_PER_DIAL * DIAL_INTERVAL)
    i = 0

    total_wavelengths = (
        (WAVELENGTH_END - WAVELENGTH_START) // WAVELENGTH_INTERVAL + 1
    )

    # Initialize Keithley once before scan starts
    initialize_keithley()

    print(f'\nScan started.')

    while wavelength <= WAVELENGTH_END:
        print(f'\n{"=" * 55}')
        print(f'Step {i+1}/{total_wavelengths} | '
              f'Dial: {dial} | '
              f'Wavelength: {wavelength} nm')
        print(f'{"=" * 55}')

        # --- Repeat block ---
        for rep in range(1, NUM_REPEATS + 1):
            print(f'\n  Repeat {rep}/{NUM_REPEATS}')

            # PD IN → Gentec screenshot
            move_pd('i')
            measure_power_gentec(wavelength, rep, file_prefix, i)

            # PD OUT → Keithley measurement
            move_pd('o')
            measure_keithley(wavelength, rep, file_prefix)

            # PD stays OUT → AVASoft measurement
            save_intensity_with_avasoft(file_prefix, i, rep)

        # --- Move to next wavelength ---
        if wavelength < WAVELENGTH_END:
            dial = dial + DIAL_INTERVAL
            wavelength = wavelength + WAVELENGTH_INTERVAL
            step_motor_up(step)

        i = i + 1

    print('\n' + '=' * 55)
    print('Scan complete!')
    print(f'Total wavelengths measured: {i}')
    print(f'Files saved with prefix:    {file_prefix}')
    print('=' * 55)


# ============================================================
# Entry point
# ============================================================
if __name__ == '__main__':
    file_prefix = get_user_inputs()
    run_scan(file_prefix)
