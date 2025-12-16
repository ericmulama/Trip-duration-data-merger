
# 🚢 Trip Duration Data Merger

This Python script is designed to automate the data enrichment process by merging transaction records with trip logistics data.
## 💡 Project Overview

This Python script is designed to automate the data enrichment process by merging transaction records with trip logistics data. The goal is to calculate the precise, business-critical duration of each transport job in whole days and integrate this metric into the primary transactions file.
## Project Goal
The primary objective is to enrich the transactions_2025.csv file by:

1. Extracting ```ACTIVATION DATE``` and ```DEACTIVATION DATE``` from the ECTS file.

2. Calculating the duration between these two dates.

3. Converting the duration into whole days, where any partial day (even one hour) is rounded up to the next full day (using the ceiling function).

4. Merging the calculated duration back into the transactions file.
## Motivation

Accurate trip duration is essential for billing, transit analysis, and logistics planning. This script ensures that duration is calculated using the most conservative metric (rounding up) to account for full days of service commitment.
## Input Files

1. transactions_2025.csv (Primary Transaction Records)
2. ECTS Extra Days_Since Oct to Nov 30,2025.xlsx (Logistics/Date Source)

## Output Files
transactions_2025_with_duration.csv (The final, enriched dataset)
## ✨ Key Logic: Whole Day Duration (The Ceiling Rule)

The calculation uses a crucial business requirement: any fraction of a day is rounded up to the next full day. This is achieved using the mathematical ceiling function ($\lceil x \rceil$).

| Duration (H:M:S) | Duration (Float Days) | Result (Whole Days) |
| :--- | :--- | :--- |
| 7 days, 00:00:00 | 7.00 days | 7 |
| 7 days, 01:00:00 | 7.04 days | **8** |
| 7 days, 23:59:59 | 7.99 days | **8** |

### Joining and Calculation Keys

| Dataset | Field Name | Role |
| :--- | :--- | :--- |
| **transactions** | `Sub T1 No` | **Joining Key (Left Table)** |
| **ECTS** | `TRIP NO` | **Joining Key (Right Table)** |
| **ECTS** | `ACTIVATION DATE` | Used for calculation, carried to output. |
| **ECTS** | `DEACTIVATION DATE` | Used for calculation, carried to output. |
| **Output (New)** | `DURATIONS (Whole Days)` | The final, calculated, and rounded duration in days. |

## 🛠️ Installation and Setup
### Prerequisites

Ensure you have Python 3.x installed. The following libraries are required for data manipulation and reading the Excel file format:

```
pip install pandas numpy openpyxl
```
### File Structure

```
/trip-data-project
├── README.md
├── transactions_report.py
├── transactions_2025.csv
└── ECTS Extra Days_Since Oct to Nov 30,2025.xlsx
```

## ⚙️ Execution and Data Pipeline

### Script Logic
The script performs a Left Join to ensure all records from the ```transactions_2025.csv``` file are retained, even if a matching trip ID is not found in the ECTS data.

| Step | Action | Logic Detail |
| :--- | :--- | :--- |
| **1. Load Data** | Reads both CSV and XLSX input files. | `pd.read_csv`, `pd.read_excel(..., engine='openpyxl')` |
| **2. Date Prep** | Converts date columns to datetime objects (`dayfirst=True` handles `dd/mm/yyyy` format). | `pd.to_datetime` |
| **3. Calculate** | Computes duration as total seconds, then converts to days (`float`). | `Timedelta.dt.total_seconds()` |
| **4. Apply Ceiling** | **Rounds up** the float duration to the nearest integer. | `numpy.ceil().astype('Int64')` |
| **5. Merge** | Joins the datasets on the common trip ID. | `transactions['Sub T1 No']` vs. `ECTS['TRIP NO']` |

### Joining Keys and Output Fields

### Joining Keys and Output Fields

| Dataset | Field Name | Role |
| :--- | :--- | :--- |
| **transactions** | `Sub T1 No` | **Joining Key (Left Table)** |
| **ECTS** | `TRIP NO` | **Joining Key (Right Table)** |
| **Output (New)** | `DURATIONS (Whole Days)` | The final calculated duration (Integer). |


## ▶️ Usage
1. Place the Python script (data_merger.py) and both input data files in the same directory.
2. Open your terminal or command line and navigate to the project directory.
3. Execute the script:

```python data_merger.py```
## 📊 Output File

The output file, transactions_2025_with_duration_whole_days.csv, will be generated in the root directory. It includes all original columns from the transactions file, plus the following three new columns:

```1. ACTIVATION DATE```

```2. DEACTIVATION DATE```

```3. DURATIONS (Whole Days)```
## Prerequisites
You need the following software and Python packages installed to run this script:

1. Python 3.x

2. pandas: For data manipulation and file I/O.

3. numpy: For mathematical operations, specifically the ceil (ceiling) function.

4. openpyxl: Required by pandas to read .xlsx Excel files.

You can install the necessary Python packages using pip:

```pip install pandas numpy openpyxl```