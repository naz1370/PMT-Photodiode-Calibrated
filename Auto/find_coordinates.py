# find_coordinates.py
import pyautogui
import time

targets = [
   
    # COSMOS buttons
    

    # AVASoft buttons
    'AVASoft in taskbar',
    'AVASoft Home button',
    'AVASoft Absolute Intensity button',
    'AVASoft Start button',
    'AVASoft File menu',
    'AVASoft Export option',
    'AVASoft ASCII option',

]

results = {}
for target in targets:
    print(f'\nMove mouse to: {target}')
    print('You have 5 seconds...')
    time.sleep(15)
    x, y = pyautogui.position()
    results[target] = (x, y)
    print(f'  → x={x}, y={y}')

print('\n' + '='*50)
print('ALL COORDINATES:')
print('='*50)
for target, (x, y) in results.items():
    print(f'{target}: x={x}, y={y}')


