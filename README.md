# MOLLER PMT Photodiode-Calibrated Spectral Characterization
## Method
- Light source: monochromator (230–510 nm, 20 nm steps)
- Reference: photodiode (PD) power measurement
- Signal: PMT cathode current (I_cathode)
- Spectral response: S(C) = 1.99e-7 × I_cathode / (P_PD × λ)
- 5 repeated measurements per wavelength


## How to Run
```bash
python spectrometer_fwhm.py --folder /path/to/txt/files --out results/
```

## How to use in Google Colab
**Part 1 — Download the script from GitHub**
!git clone https://github.com/naz1370/PMT-Photodiode-Calibrated.git

**Part 2 — Upload your .txt spectrometer files**
from google.colab import files
uploaded = files.upload()

**Part 3 — Run the analysis**
!python PMT-Photodiode-Calibrated/spectrometer_fwhm.py --folder . --out results/

Computes peak wavelength, FWHM, and Δλ for each nominal wavelength.

**Part 4 — Convert results to Excel**
import pandas as pd
df = pd.read_csv('results/results_summary.csv')
df.to_excel('results/results_summary.xlsx', index=False)

**Part 5 — Download the Excel file**
from google.colab import files
files.download('results/results_summary.xlsx')

