# 🔬 Physics Lab Computational Analysis
### University of Göttingen | B.Sc. Physics

This repository contains automated data analysis scripts developed for Experimental Physics lab modules at the University of Göttingen. The project replaces manual calculations with high-precision scientific computing, utilizing **weighted linear regressions**, **effective variance modeling**, and **automatic error propagation**.

---

## 🚀 Core Features
* **Rigorous Error Propagation:** Implementation of the `uncertainties` library to handle covariance matrices and Gaussian error propagation across all physical constants.
* **Effective Variance Method:** Advanced fitting techniques that account for uncertainties in both the independent ($x$) and dependent ($y$) variables, critical for Arrhenius plots.
* **Automated Visualization:** Scripts generate high-resolution plots (300 DPI) and automatically manage directory structures for `/plots` and `/data`.
* **Professional Data Handling:** Uses `pandas` for clean ingestion and cleaning of experimental CSV datasets.

---

## 📂 Project Structure
The repository is organized by experimental module to provide a clear, professional portfolio for academic and industrial review:

```text
.
├── Lab-analysis/
│   ├── v5-specific-heat-gas-thermometer/       # Module v5
│   │   ├── data/                               # Raw experimental CSVs
│   │   ├── plots/                              # Generated PDFs and PNGs
│   │   ├── v5_specific_heat.py                 # Adiabatic exponent analysis
│   │   ├── v5_gas_thermometer_heating.py       # Absolute zero (Heating)
│   │   └── v5_gas_thermometer_cooling.py       # Absolute zero (Cooling)
│   └── v7-vapor-pressure-of-water/             # Module v7
│       ├── data/                               # Pressure & Resistance datasets
│       ├── plots/                              # Arrhenius & Vapor pressure plots
│       ├── v7_heating_improved.py              # Enthalpy analysis (Heating)
│       └── v7_cooling_improved.py              # Enthalpy analysis (Cooling)
├── .gitignore                                  # Python-standard junk filter
├── LICENSE                                     # MIT License
└── README.md                                   # Project Documentation
