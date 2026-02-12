"""
Project: Lab Analysis of The Experiment The Specific Heat of Air and Gas Thermometer.
Author: Anass El Warraqi
Date: February 2026
Purpose: The experiment uses a gas thermometer to determine the absolute zero temperature (Heating Phase).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat, correlated_values
import os

# --- 1. Configuration & File Management ---
FILENAME = 'data/v5_heating.csv'  # Adjusted path standard
OUTPUT_DIR = 'plots'
PLOT_FILE = 'v5_gas_thermometer_heating.pdf'
TXT_FILE = 'results_gas_thermometer_heating.txt'

# Create the output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Created directory: {OUTPUT_DIR}")

SIGMA_P = 5.0   # Uncertainty in Pressure (hPa)
SIGMA_T = 1.0   # Uncertainty in Temperature (°C)

# --- 2. Load Data ---
def load_lab_data(filename):
    try:
        df = pd.read_csv(filename, sep=None, engine='python')
        df.columns = df.columns.str.strip()
        print(f"Successfully loaded: {filename}")
        return df
    except FileNotFoundError as e:
        print(f"Error loading file: {e}")
        return None

df = load_lab_data(FILENAME)

if df is not None:
    T_celsius = df["Temperatur (C)"].to_numpy()
    p_hPa = df["Druck (hPa)"].to_numpy()

    # --- 3. Define Model & Fit ---
    def linear_model(T, m, b):
        return m * T + b

    # Perform weighted fit
    popt, pcov = curve_fit(linear_model, T_celsius, p_hPa,
                           sigma=[SIGMA_P]*len(p_hPa), absolute_sigma=True)

    # --- 4. Error Propagation ---
    slope, intercept = correlated_values(popt, pcov)

    # Calculate Absolute Zero (T0)
    # Physics: P = 0 => T0 = -b / m
    T0 = -intercept / slope

    # Deviation
    lit_value = -273.15
    sigma_deviation = abs(T0.n - lit_value) / T0.s

    # --- 5. Formatting & Saving Results ---
    results_text = f"""
------------------------------------------------------------
Analysis Results: Gas Thermometer (Heating)
Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
File Analyzed: {FILENAME}
------------------------------------------------------------
Fit Parameters:
  Slope (m):     {slope:.4f} hPa/°C
  Intercept (b): {intercept:.4f} hPa

Physics Results:
  Calculated Absolute Zero: {T0:.2f} °C
  Literature Value:         {lit_value} °C
  Deviation:                {sigma_deviation:.1f} sigma
------------------------------------------------------------
"""
    print(results_text)

    # Save to text file
    txt_path = os.path.join(OUTPUT_DIR, TXT_FILE)
    with open(txt_path, "w") as f:
        f.write(results_text)
    print(f"Results saved to: {txt_path}")

    # --- 6. Plotting ---
    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)

    # Plot Data
    ax.errorbar(T_celsius, p_hPa, yerr=SIGMA_P, xerr=SIGMA_T,
                fmt='o', color='orange', ecolor='gray', capsize=3, label="Messdaten")

    # Plot Fit Line
    t_line = np.linspace(min(T_celsius), max(T_celsius), 100)
    p_line = linear_model(t_line, slope.n, intercept.n)

    ax.plot(t_line, p_line, color="green",
            label=f"Fit: $T_0 = {T0.n:.1f} \\pm {T0.s:.1f} ^\\circ C$")

    # Labels and Styling
    ax.set_title("Gasthermometer Erwärmung: Druck gegen Temperatur", fontsize=14, fontweight="bold")
    ax.set_xlabel("Temperatur [$^\\circ C$]", fontsize=12)
    ax.set_ylabel("Druck [$hPa$]", fontsize=12)
    ax.legend(loc="upper left")
    ax.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()

    # Save Plot
    plot_path = os.path.join(OUTPUT_DIR, PLOT_FILE)
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved successfully to: {plot_path}")

    plt.show()