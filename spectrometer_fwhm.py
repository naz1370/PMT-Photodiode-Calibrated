"""
spectrometer_fwhm.py
--------------------
Reads Avasoft ASCII spectrometer files, computes peak wavelength,
FWHM, and delta-lambda for each nominal wavelength (5 repeats each).

Usage
-----
    python spectrometer_fwhm.py --folder /path/to/txt/files

Output
------
    results_summary.csv   — one row per nominal wavelength (mean ± std)
    results_all.csv       — one row per file
    spectra_summary.png   — 3-panel plot (Δλ, FWHM, intensity)
    spectra_individual/   — one plot per nominal wavelength
"""

import argparse
import os
import re
import glob
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# ── Parser ─────────────────────────────────────────────────────────────────
def parse_avasoft(filepath):
    """Return (wavelengths, net_signal) from an Avasoft ASCII file."""
    wvs, net = [], []
    with open(filepath, 'r', errors='replace') as f:
        for line in f:
            parts = line.strip().replace(',', '.').split(';')
            if len(parts) < 3:
                continue
            try:
                wvs.append(float(parts[0]))
                net.append(float(parts[1]) - float(parts[2]))  # Sample - Dark
            except ValueError:
                continue
    return np.array(wvs), np.array(net)


# ── FWHM ───────────────────────────────────────────────────────────────────
def find_fwhm(wvs, signal):
    """
    Returns (peak_wv, peak_val, fwhm, lam_left, lam_right).
    Uses linear interpolation for sub-pixel accuracy.
    """
    idx  = np.argmax(signal)
    peak_wv  = wvs[idx]
    peak_val = signal[idx]
    half     = peak_val / 2.0

    lam_left = None
    for i in range(idx, 0, -1):
        if signal[i - 1] <= half <= signal[i]:
            dx = wvs[i] - wvs[i - 1]
            dy = signal[i] - signal[i - 1]
            lam_left = wvs[i - 1] + (half - signal[i - 1]) * dx / dy
            break

    lam_right = None
    for i in range(idx, len(signal) - 1):
        if signal[i] >= half >= signal[i + 1]:
            dx = wvs[i + 1] - wvs[i]
            dy = signal[i + 1] - signal[i]
            lam_right = wvs[i] + (half - signal[i]) * dx / dy
            break

    fwhm = (lam_right - lam_left) if (lam_left and lam_right) else None
    return peak_wv, peak_val, fwhm, lam_left, lam_right


# ── Nominal wavelength from filename ──────────────────────────────────────
def get_nominal(fname):
    m = re.search(r'(\d+)nm', os.path.basename(fname))
    return int(m.group(1)) if m else None


# ── Main ───────────────────────────────────────────────────────────────────
def main(folder, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, 'spectra_individual'), exist_ok=True)

    files = sorted(glob.glob(os.path.join(folder, '*.txt')))
    if not files:
        print(f"No .txt files found in {folder}")
        return

    print(f"Found {len(files)} files in {folder}\n")

    # ── Process each file ────────────────────────────────────────────
    rows = []
    for fp in files:
        wvs, net = parse_avasoft(fp)
        if len(wvs) == 0:
            print(f"  WARNING: could not parse {fp}")
            continue
        pw, pv, fwhm, ll, lr = find_fwhm(wvs, net)
        nw = get_nominal(fp)
        rows.append({
            'file':      os.path.basename(fp),
            'nominal_wv': nw,
            'peak_wv':   pw,
            'peak_int':  pv,
            'fwhm':      fwhm,
            'lam_left':  ll,
            'lam_right': lr,
            '_wvs':      wvs,
            '_net':      net,
        })

    df_all = pd.DataFrame([{k: v for k, v in r.items() if not k.startswith('_')}
                            for r in rows])
    df_all['delta_lam'] = df_all['peak_wv'] - df_all['nominal_wv']

    # ── Group by nominal wavelength ───────────────────────────────────
    nominal_wvs = sorted(df_all['nominal_wv'].dropna().unique().astype(int))

    summary_rows = []
    for nw in nominal_wvs:
        grp = df_all[df_all['nominal_wv'] == nw]
        fwhms = grp['fwhm'].dropna()
        summary_rows.append({
            'nominal_wv':      nw,
            'n_files':         len(grp),
            'peak_wv_mean':    grp['peak_wv'].mean(),
            'peak_wv_std':     grp['peak_wv'].std(ddof=1),
            'delta_lam_mean':  grp['delta_lam'].mean(),
            'delta_lam_std':   grp['delta_lam'].std(ddof=1),
            'fwhm_mean':       fwhms.mean()         if len(fwhms) else np.nan,
            'fwhm_std':        fwhms.std(ddof=1)    if len(fwhms) > 1 else 0,
            'peak_int_mean':   grp['peak_int'].mean(),
            'peak_int_std':    grp['peak_int'].std(ddof=1),
        })

    df_sum = pd.DataFrame(summary_rows)

    # ── Print table ───────────────────────────────────────────────────
    print(f"{'λ_nom':>8} {'peak_mean':>10} {'Δλ_mean':>9} {'FWHM_mean':>10} "
          f"{'FWHM_std':>9} {'int_mean':>10}")
    for _, r in df_sum.iterrows():
        print(f"{int(r.nominal_wv):>8} {r.peak_wv_mean:>10.3f} "
              f"{r.delta_lam_mean:>+9.4f} {r.fwhm_mean:>10.4f} "
              f"{r.fwhm_std:>9.4f} {r.peak_int_mean:>10.1f}")

    # ── Save CSVs ─────────────────────────────────────────────────────
    df_sum.to_csv(os.path.join(out_dir, 'results_summary.csv'),
                  index=False, float_format='%.5f')
    df_all.to_csv(os.path.join(out_dir, 'results_all.csv'),
                  index=False, float_format='%.5f')
    print(f"\nSaved: {os.path.join(out_dir, 'results_summary.csv')}")
    print(f"Saved: {os.path.join(out_dir, 'results_all.csv')}")

    # ── 3-panel summary plot ──────────────────────────────────────────
    nws     = df_sum['nominal_wv'].values
    fig, axes = plt.subplots(3, 1, figsize=(8, 9), sharex=True)

    ax = axes[0]
    ax.errorbar(nws, df_sum['delta_lam_mean'], yerr=df_sum['delta_lam_std'],
                fmt='o-', color='#0C447C', markersize=4, linewidth=1,
                ecolor='#791F1F', elinewidth=1, capsize=3, capthick=0.8)
    ax.axhline(0, color='grey', linewidth=0.5, linestyle='--')
    ax.set_ylabel('Δλ (nm)\n(actual − nominal)', fontsize=10)
    ax.set_title('Wavelength offset  Δλ', fontsize=10)
    ax.grid(True, linewidth=0.3, alpha=0.4)

    ax = axes[1]
    ax.errorbar(nws, df_sum['fwhm_mean'], yerr=df_sum['fwhm_std'],
                fmt='o-', color='#1a6b3c', markersize=4, linewidth=1,
                ecolor='#791F1F', elinewidth=1, capsize=3, capthick=0.8)
    ax.set_ylabel('FWHM (nm)', fontsize=10)
    ax.set_title('Monochromator bandwidth (FWHM)', fontsize=10)
    ax.grid(True, linewidth=0.3, alpha=0.4)

    ax = axes[2]
    ax.errorbar(nws, df_sum['peak_int_mean'], yerr=df_sum['peak_int_std'],
                fmt='o-', color='#6b3a1a', markersize=4, linewidth=1,
                ecolor='#791F1F', elinewidth=1, capsize=3, capthick=0.8)
    ax.set_ylabel('Peak intensity (counts)', fontsize=10)
    ax.set_xlabel('Nominal wavelength (nm)', fontsize=11)
    ax.set_xticks(nws)
    ax.set_xticklabels([str(int(w)) for w in nws], rotation=45,
                       ha='right', fontsize=8)
    ax.set_title('Source peak intensity', fontsize=10)
    ax.grid(True, linewidth=0.3, alpha=0.4)

    plt.tight_layout()
    out_png = os.path.join(out_dir, 'spectra_summary.png')
    plt.savefig(out_png, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_png}")

    # ── Individual spectrum plots ─────────────────────────────────────
    colors = ['#0C447C', '#791F1F', '#1a6b3c', '#6b3a1a', '#4b1a6b']
    for nw in nominal_wvs:
        grp_rows = [r for r in rows if r['nominal_wv'] == nw]
        fig, ax = plt.subplots(figsize=(6, 3.5))
        for k, r in enumerate(grp_rows):
            ax.plot(r['_wvs'], r['_net'], color=colors[k % 5],
                    linewidth=0.8, alpha=0.85, label=f"rep {k+1}")
            if r['fwhm']:
                ax.hlines(r['peak_int'] / 2, r['lam_left'], r['lam_right'],
                          color=colors[k % 5], linewidth=2, linestyle='--')
                ax.axvline(r['peak_wv'], color=colors[k % 5],
                           linewidth=0.6, linestyle=':')
        ax.set_xlim(nw - 40, nw + 40)
        s = df_sum[df_sum['nominal_wv'] == nw].iloc[0]
        ax.set_title(
            f'{nw} nm  |  peak={s.peak_wv_mean:.2f} nm  |  '
            f'FWHM={s.fwhm_mean:.2f} nm  |  Δλ={s.delta_lam_mean:+.3f} nm',
            fontsize=8)
        ax.set_xlabel('Wavelength (nm)', fontsize=9)
        ax.set_ylabel('Net signal (counts)', fontsize=9)
        ax.legend(fontsize=7, ncol=2)
        ax.grid(True, linewidth=0.3, alpha=0.4)
        plt.tight_layout()
        out_sp = os.path.join(out_dir, 'spectra_individual', f'{nw}nm.png')
        plt.savefig(out_sp, dpi=150, bbox_inches='tight')
        plt.close()

    print(f"Saved individual spectra → {os.path.join(out_dir, 'spectra_individual')}/")


# ── Entry point ────────────────────────────────────────────────────────────
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Analyse Avasoft spectrometer ASCII files: peak, FWHM, Δλ.')
    parser.add_argument('--folder', default='.',
                        help='Folder containing the .txt files (default: current dir)')
    parser.add_argument('--out', default='output',
                        help='Output folder for plots and CSVs (default: output/)')
    args = parser.parse_args()
    main(args.folder, args.out)
