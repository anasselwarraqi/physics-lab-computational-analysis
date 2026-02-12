🔬 Physics Lab Computational AnalysisUniversity of Göttingen | B.Sc. PhysicsThis repository contains automated data analysis scripts developed for the Experimental Physics lab modules. The project focuses on replacing manual calculations with high-precision scientific computing, utilizing weighted linear regressions and automatic error propagation.🚀 FeaturesRigorous Error Propagation: Full implementation of the uncertainties library to handle covariance matrices and Gaussian error propagation.Effective Variance Method: Advanced fitting techniques that account for uncertainties in both the independent ($x$) and dependent ($y$) variables.Automated Visualization: High-resolution plotting with automated folder management for professional reporting.Data Integrity: Structured data handling using pandas for clean ingestion of experimental CSV files.📂 Project StructureThe repository is organized by experimental module to ensure a professional and navigable portfolio:Plaintext.
├── Lab-analysis/
│   ├── v5-specific-heat-gas-thermometer/       # Specific Heat & Absolute Zero
│   │   ├── data/                               # Raw experimental CSVs
│   │   ├── plots/                              # Generated PDFs and PNGs
│   │   └── v5_specific_heat.py                 # Main analysis scripts
│   └── v7-vapor-pressure-of-water/             # Thermodynamics of Water
│       ├── data/                               # Pressure/Ohmzahl datasets
│       ├── plots/                              # Arrhenius plots
│       └── v7_heating_improved.py              # Effective Variance analysis
├── .gitignore                                  # Python-standard junk filter
├── LICENSE                                     # MIT License
└── README.md                                   # Documentation
📊 Experimental Modules1. Specific Heat of Air (Module v5)Determining the adiabatic exponent ($\kappa$) and degrees of freedom ($f$) for air.Theory: $\Delta p = \frac{\kappa - 1}{V} \cdot \Delta Q$.Results: Automatically calculates $\kappa$ and provides a $\sigma$-deviation check against literature values ($1.40$).2. Gas Thermometer (Module v5)Determination of Absolute Zero ($T_0$) through the cooling and heating phases of an ideal gas.Logic: Linear extrapolation of $P(T)$ to zero pressure using correlated fit parameters.3. Vapor Pressure of Water (Module v7)Analysis of the Clausius-Clapeyron relation to determine the Enthalpy of Vaporization ($\Delta H_{vap}$).Advanced Fitting: Uses an Arrhenius plot ($\ln(p)$ vs $1/T$) with effective variance weighting to handle high-temperature measurement fluctuations.📈 Visual ResultsArrhenius Analysis (Module v7)Example of a cooling phase fit showing strong agreement with theoretical vapor pressure curves.🛠️ Installation & UsageClone the repository:Bashgit clone https://github.com/anasselwarraqi/physics-lab-computational-analysis.git
Install dependencies:Bashpip install numpy pandas matplotlib scipy uncertainties
Run an analysis:Bashpython Lab-analysis/v7-vapor-pressure-of-water/v7_heating_improved.py
📜 LicenseThis project is licensed under the MIT License - see the LICENSE file for details.Author: Anass El WarraqiDate: February 2026
