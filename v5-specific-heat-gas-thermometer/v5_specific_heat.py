"""
Project: Lab Analysis of the experiment "Specific Heat of Air" (Spezifische Wärme der Luft)
Author: Anass El Warraqi
Date: February 2026
Purpose: Determine the adiabatic exponent (kappa) and degrees of freedom (f) of air.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat, correlated_values
import os

# --- 1. Configurations & File Management  ---
FILENAME = "data/v5_specific_heat.csv"  # Ensure this matches your actual file location
OUTPUT_DIR = 'plots'
PLOT_FILE = 'v5_specific_heat.pdf'
TXT_FILE = 'results_specific_heat.txt'  # <--- NEW: Text file name

# Create the output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Created directory: {OUTPUT_DIR}")

# Constants (SI Units)
# Uncertainties
SIGMA_U = 3.0          # Uncertainty in Voltage (V)
SIGMA_H = 0.5          # Uncertainty in height (mm)
V_ERR   = 0.000129     # Uncertainty in Volume (m^3)

# Equipment Constants
C = 20e-6              # Capacity (F)
RHO_WATER = 1000.0     # Density of water (kg/m^3)
G = 9.81               # Gravity (m/s^2)
VOLUME_VAL = 3.2e-3    # Volume (m^3)

# Create a ufloat for Volume to propagate its error later
VOLUME = ufloat(VOLUME_VAL, V_ERR)

# --- 2. Load Data ---
def load_lab_data(filename):
    try:
        df = pd.read_csv(filename, sep=None, engine='python')
        df.columns = df.columns.str.strip()
        print(f"Successfully loaded {filename}")
        return df
    except FileNotFoundError as e:
        print(f"Error loading file: {e}")
        return None

df = load_lab_data(FILENAME)

# Check if data loaded successfully
if df is not None:
    # Extract arrays
    U_volt = df["Spannung (V)"].to_numpy()
    Delta_H_mm = df["Delta_H (mm)"].to_numpy()

    # --- 3. Calculations & Conversions ---
    # X-Axis: Energy Q = 0.5 * C * U^2
    Delta_Q = 0.5 * C * (U_volt ** 2)
    sigma_Q = C * U_volt * SIGMA_U

    # Y-Axis: Pressure p = rho * g * h
    Delta_p = RHO_WATER * G * (Delta_H_mm / 1000.0)
    sigma_p = np.full(len(Delta_p), RHO_WATER * G * (SIGMA_H / 1000.0))

    # --- 4. Fitting ---
    def linear_model(x, m, b):
        return m * x + b

    # Perform weighted fit
    popt, pcov = curve_fit(linear_model, Delta_Q, Delta_p,
                           sigma=sigma_p, absolute_sigma=True)

    slope, intercept = correlated_values(popt, pcov)

    # --- 5. Physics Analysis (Automatic Error Propagation) ---
    # A) Calculate Kappa
    kappa = slope * VOLUME + 1

    # Deviation Calculation
    sigma_dev_k = abs(kappa.n - 1.40) / kappa.s

    # B) Calculate Degrees of Freedom (f)
    f_measured = 2.0 / (kappa - 1)

    # --- 6. Formatting & Saving Results (Text File) ---
    results_text = f"""
------------------------------------------------------------
Analysis Results: Specific Heat of Air
Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
File Analyzed: {FILENAME}
------------------------------------------------------------
Fit Parameters:
  Slope (m):     {slope:.2f} Pa/J
  Intercept (b): {intercept:.2f} Pa

Physics Results:
  Adiabatic Exponent (kappa): {kappa:.4f}
  Literature Value (Air):     1.400
  Deviation:                  {sigma_dev_k:.1f} sigma

  Degrees of Freedom (f):     {f_measured:.3f}
  Expected Value (Diatomic):  5.00
------------------------------------------------------------
"""
    # Print to console
    print(results_text)

    # Save to text file
    txt_path = os.path.join(OUTPUT_DIR, TXT_FILE)
    with open(txt_path, "w") as f:
        f.write(results_text)
    print(f"Results saved to: {txt_path}")

    # --- 7. Plotting ---
    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)

    # Plot Data with Error Bars
    ax.errorbar(Delta_Q, Delta_p, xerr=sigma_Q, yerr=sigma_p,
                fmt="o", color="teal", ecolor="gray",
                capsize=3, alpha=0.8, label="Messdaten")

    # Plot Fit Line
    q_line = np.linspace(min(Delta_Q), max(Delta_Q), 100)
    p_line = linear_model(q_line, slope.n, intercept.n)

    ax.plot(q_line, p_line, color="darkred",
            label=f"Linear Fit: $\\kappa = {kappa.n:.2f} \\pm {kappa.s:.2f}$")

    # Styling
    ax.set_title("Spezifische Wärme: Druckanstieg vs. Heizenergie", fontsize=14, fontweight="bold")
    ax.set_xlabel("Elektrische Energie $\\Delta Q$ [J]", fontsize=12)
    ax.set_ylabel("Druckänderung $\\Delta p$ [Pa]", fontsize=12)
    ax.legend(loc="upper left", frameon=True)
    ax.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()

    # Save Plot
    plot_path = os.path.join(OUTPUT_DIR, PLOT_FILE)
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved successfully to: {plot_path}")

    plt.show()