# Trip Duration Data Merger

[![Project Status](https://img.shields.io/badge/Status-Complete-brightgreen)](https://github.com/your-username/your-repo-name)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)

## Project Overview

This Python script is designed to automate the process of merging financial/transaction data (`transactions_2025.csv`) with trip logistics data (`ECTS Extra Days_Since Oct to Nov 30,2025.xlsx`). The primary goal is to **calculate the duration of each trip in whole days** and integrate this metric directly into the main transactions log.

## Key Feature: Whole Day Duration Calculation (Ceiling Logic)

The script implements a specific business logic for calculating duration:

1.  It determines the raw time difference between the `ACTIVATION DATE` and `DEACTIVATION DATE`.
2.  It converts this time difference into a floating-point number of days (e.g., 8.01 days).
3.  **Crucially, it uses the ceiling function ($\lceil x \rceil$) to round up any partial day to the next whole day.** This ensures that any fraction of a day is treated as a full day (e.g., 8.01 days rounds up to 9 days).

## File Structure

For the script to run without modification, ensure your local project directory contains the following files:

/your-project-folder├── README.md
                    ├── data_merger.py
                    ├── transactions_2025.csv
                    └── ECTS Extra Days_Since Oct to Nov 30,2025.xlsx
## Prerequisites

You need the following dependencies installed in your Python environment:

pip install pandas numpy openpyxl
Script Logic: Data PipelineThe script performs a Left Join, ensuring all transaction records are retained.StepActionKey Fields & Logic1. Load DataReads the CSV and XLSX input files.pd.read_csv, pd.read_excel2. Date PreparationConverts date columns to datetime objects (dayfirst=True handles dd/mm/yyyy format).pd.to_datetime3. Calculate DurationComputes duration as total seconds, then divides by 86400 to get days (float).Timedelta.dt.total_seconds()4. Apply CeilingRounds up the float duration using the ceiling function.numpy.ceil().astype('Int64')5. MergeJoins data using a Left Join.left_on='Sub T1 No' vs. right_on='TRIP NO'6. OutputSaves the enriched data to CSV.transactions_2025_with_duration_whole_days.csvJoining Keys and Output FieldsDatasetField NameRoletransactionsSub T1 NoJoining Key (Left Table)ECTSTRIP NOJoining Key (Right Table)Output (New)DURATIONS (Whole Days)The final calculated duration (Integer).Usage (Running the Script)Place the Python script (data_merger.py) and both input data files in the same directory.Open your terminal or command line and navigate to the project directory.Execute the script:Bashpython data_merger.py
Output FileA new file named transactions_2025_with_duration_whole_days.csv will be generated. It includes all original columns from the transactions file, plus the following three new columns:ACTIVATION DATEDEACTIVATION DATEDURATIONS (Whole Days)
