# Campus Energy Audit Dashboard

An interactive web-based dashboard for analysing campus energy consumption data, built with Streamlit and Plotly. It provides real-time visualisations, filterable metrics, and data-driven actionable insights to help identify energy reduction opportunities across campus locations and equipment.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Data Format](#data-format)
- [Configuration](#configuration)
- [License](#license)

---

## Features

- **Summary Metric Cards** -- Highest consumer, lowest consumer, total monthly consumption, and total installed power at a glance.
- **Interactive Charts** -- Four Plotly visualisations:
  - Monthly consumption by location (horizontal bar chart)
  - Monthly consumption by equipment (donut pie chart)
  - Daily vs monthly consumption comparison (grouped bar chart)
  - Installed power capacity by location (horizontal bar chart)
- **Sidebar Filters** -- Filter data dynamically by location/department and appliance/equipment type.
- **Data Validation** -- Automatic validation and cleaning of uploaded datasets with clear error messages for malformed data.
- **Derived Column Computation** -- Automatically calculates Power (kW), Total Power (kW), Daily Consumption (kWh), and Monthly Consumption (kWh) from user-provided base data.
- **Actionable Insights Engine** -- Generates data-driven recommendations including:
  - Identification of high-consumption locations and equipment
  - Utilisation analysis with estimated savings from reduced usage hours
  - Energy concentration analysis across equipment types
  - Savings projections at 5% and 10% reduction targets
- **Template Downloads** -- Downloadable CSV and Excel templates pre-populated with sample data.
- **Flexible Data Input** -- Supports CSV, XLS, and XLSX file uploads. Falls back to a bundled sample dataset when no file is uploaded.
- **Detailed Data Table** -- Full audit data table with formatted numeric columns.

---

## Project Structure

```
EnergyDashboard/
├── app.py                          # Main Streamlit application entry point
├── config.py                       # Column name constants and configuration
├── requirements.txt                # Python dependencies
├── Campus_Energy_Audit_Data.xlsx   # Bundled sample dataset
├── .env                            # Environment variables
├── .gitignore                      # Git ignore rules
├── components/
│   ├── __init__.py
│   ├── charts.py                   # Plotly chart rendering functions
│   ├── header.py                   # Page header, template downloads, file upload
│   ├── insights.py                 # Actionable insights display component
│   ├── metrics.py                  # Summary metric card rendering
│   └── styles.py                   # Custom CSS styling
└── utils/
    ├── __init__.py
    ├── data_processing.py          # Data validation, derived columns, insight generation
    └── template_helpers.py         # Template DataFrame builders and download helpers
```

---

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/minidusjr/EnergyDashboard.git
   cd EnergyDashboard
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # macOS / Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

**Start the dashboard:**

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

**Using the dashboard:**

1. The dashboard loads with the bundled sample dataset by default.
2. Upload your own CSV or Excel file using the upload area in the header.
3. Use the sidebar filters to narrow the analysis by location or equipment type.
4. Download CSV or Excel templates from the header section to prepare your own data.

---

## Data Format

Uploaded files must contain the following columns:

| Column Name              | Type    | Description                              |
|--------------------------|---------|------------------------------------------|
| Location / Department    | String  | Campus location or department name       |
| Appliance / Equipment    | String  | Name of the appliance or equipment       |
| Power (W)                | Numeric | Power rating in watts (must be positive) |
| Quantity                 | Numeric | Number of units (must be positive)       |
| Daily Usage (Hours)      | Numeric | Hours of daily operation (non-negative)  |
| Monthly Days Open        | Numeric | Operating days per month (must be positive) |

The following columns are automatically computed and do not need to be provided:

- Power (kW)
- Total Power (kW)
- Daily Consumption (kWh)
- Monthly Consumption (kWh)

---

## Configuration

Column name constants and the list of required/computed columns are defined in `config.py`. Modify this file if your data uses different column headers.

---

## License

This project is developed for the University of Vocational Technology energy audit initiative. 
All Rights Reserved by Minidu Hettiarachchi
