"""
Project: Lab Analysis of the experiment The Vapor Pressure of Water.
Author: Anass El Warraqi (Improved Version)
Date: February 2026
Purpose: Determine Enthalpy of Vaporization (Delta H) - Cooling Phase.
         Features: Automatic folder creation, high-res plotting, and results text file.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat, correlated_values
import os

# --- 1. Configuration & File Management ---
FILENAME = 'data/v7_cooling.csv'
OUTPUT_DIR = 'plots'
PLOT_FILE = 'v7_vapor_pressure_cooling.pdf'
TXT_FILE = 'results_vapor_pressure_cooling.txt'

# Create the output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Created directory: {OUTPUT_DIR}")

# Constants
R_GAS = 8.31446       # J / (mol K)
LIT_VAL_100C = 40.66  # kJ/mol (Literature value at 100°C)

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
    p_bar = df['Druck (Bar)'].to_numpy()
    R_ohm = df['Ohmzahl (Ohm)'].to_numpy()

    # --- 3. Conversions ---
    def resistance_to_temperature(R_ohm):
        A = 3.9083e-3
        B = -5.775e-7
        R0 = 1000.0
        discriminant = A**2 - 4 * B * (1 - R_ohm / R0)
        T_celsius = (-A + np.sqrt(discriminant)) / (2 * B)
        return T_celsius

    T_celsius = resistance_to_temperature(R_ohm)
    T_kelvin = T_celsius + 273.15

    # --- 4. Uncertainty Calculation ---
    sigma_T = np.sqrt((1.0/3.85)**2 + (0.3 + 0.005 * T_celsius)**2)
    sigma_p = 0.01 * p_bar

    # --- 5. Prepare Arrhenius Plot Data ---
    x_val = 1.0 / T_kelvin
    y_val = np.log(p_bar)

    x_err = sigma_T / (T_kelvin**2)
    y_err = sigma_p / p_bar

    # --- 6. Fitting with Effective Variance ---
    def linear_model(x, m, c):
        return m * x + c

    # Pass 1: Initial Estimate
    popt_init, _ = curve_fit(linear_model, x_val, y_val, sigma=y_err, absolute_sigma=True)
    m_init = popt_init[0]

    # Pass 2: Effective Variance
    sigma_eff = np.sqrt(y_err**2 + (m_init * x_err)**2)

    popt, pcov = curve_fit(linear_model, x_val, y_val, sigma=sigma_eff, absolute_sigma=True)
    slope, intercept = correlated_values(popt, pcov)

    # --- 7. Calculate Enthalpy & Format Results ---
    Delta_H = -slope * R_GAS
    Delta_H_kJ = Delta_H / 1000.0

    sigma_dev = abs(Delta_H_kJ.n - LIT_VAL_100C) / Delta_H_kJ.s

    results_text = f"""
------------------------------------------------------------
Analysis Results: Vapor Pressure (Cooling)
Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
File Analyzed: {FILENAME}
------------------------------------------------------------
Fit Parameters:
  Slope (m):     {slope:.4f} K
  Intercept (c): {intercept:.4f}

Physics Results:
  Enthalpy of Vaporization: {Delta_H_kJ:.2f} kJ/mol
  Literature Value (100°C): {LIT_VAL_100C} kJ/mol
  Deviation:                {sigma_dev:.1f} sigma
------------------------------------------------------------
"""
    # Print and Save
    print(results_text)
    txt_path = os.path.join(OUTPUT_DIR, TXT_FILE)
    with open(txt_path, "w") as f:
        f.write(results_text)
    print(f"Results saved to: {txt_path}")

    # --- 8. Plotting ---
    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)

    ax.errorbar(x_val, y_val, xerr=x_err, yerr=y_err, fmt='o',
                markersize=4, color='blue', ecolor='gray',
                capsize=2, label='Messdaten', alpha=0.8)

    x_fit = np.linspace(min(x_val), max(x_val), 100)
    y_fit = linear_model(x_fit, slope.n, intercept.n)

    ax.plot(x_fit, y_fit, color='cyan', linewidth=2,
            label=fr'Fit: $\Delta H = {Delta_H_kJ.n:.2f} \pm {Delta_H_kJ.s:.2f}$ kJ/mol')

    ax.set_title("Arrheniusplot Abkühlung: $\\ln(p)$ vs $1/T$", fontsize=14, fontweight='bold')
    ax.set_xlabel("Reziproke Temperatur $1/T$ [$K^{-1}$]", fontsize=12)
    ax.set_ylabel("Log-Druck $\\ln(p/1\\,bar)$", fontsize=12)
    ax.legend(loc="upper right", frameon=True)
    ax.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()

    # Save Plot
    plot_path = os.path.join(OUTPUT_DIR, PLOT_FILE)
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved successfully to: {plot_path}")

    plt.show()