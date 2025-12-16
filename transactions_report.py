import pandas as pd
import numpy as np
import os

# File Paths
TRANSACTIONS_FILE = "transactions_2025.csv"
ECTS_FILE = "ECTS Extra Days_Since Oct to Nov 30,2025.xlsx"
OUTPUT_FILE = "transactions_2025_with_duration.csv"

print("--- Starting Data Merge Script ---")

# LOAD DATASETS
try:
    df_transactions = pd.read_csv(TRANSACTIONS_FILE)
    df_ects = pd.read_excel(ECTS_FILE, sheet_name=0, engine="openpyxl")
    print(f"\n[INFO] Successfully loaded: {TRANSACTIONS_FILE} and {ECTS_FILE}")

except FileNotFoundError as e:
    print(f"\n[FATAL ERROR] File not found. Please check your file names and path: {e}")
    exit()
except ImportError:
    print("\n[FATAL ERROR] openpyxl library is required to read XLSX files.")
    print("Please run: pip install openpyxl")
    exit()
except Exception as e:
    print(f"\n[FATAL ERROR] An error occurred during file loading: {e}")
    exit()


# Dates and Duration Calculation

df_ects["ACTIVATION DATE"] = pd.to_datetime(
    df_ects["ACTIVATION DATE"], dayfirst=True, errors="coerce"
)
df_ects["DEACTIVATION DATE"] = pd.to_datetime(
    df_ects["DEACTIVATION DATE"], dayfirst=True, errors="coerce"
)

# Calculate the Duration
df_ects["Duration_Timedelta"] = (
    df_ects["DEACTIVATION DATE"] - df_ects["ACTIVATION DATE"]
)

# Convert to total days (float)
SECONDS_PER_DAY = 24 * 60 * 60
df_ects["Duration_Float_Days"] = (
    df_ects["Duration_Timedelta"].dt.total_seconds() / SECONDS_PER_DAY
)

# Apply Ceiling function to round up any partial day,
# then convert to a nullable integer (Int64) for whole days.
df_ects["DURATIONS (Whole Days)"] = np.ceil(df_ects["Duration_Float_Days"]).astype(
    "Int64"
)
print("\n--- ECTS Data Sample (Duration in Whole Days) ---")
print(df_ects[["TRIP NO", "Duration_Float_Days", "DURATIONS (Whole Days)"]].head())

# MERGE DATASETS

# Define the columns to select from the ECTS file for merging
columns_to_merge = [
    "TRIP NO",
    "ACTIVATION DATE",
    "DEACTIVATION DATE",
    "DURATIONS (Whole Days)",
]

# Connecting fields are 'Sub T1 No' and 'TRIP NO'
merged_df = df_transactions.merge(
    df_ects[columns_to_merge], left_on="Sub T1 No", right_on="TRIP NO", how="left"
)

# Clean up: Drop the redundant 'TRIP NO' column
merged_df.drop(columns=["TRIP NO"], inplace=True)


# SAVE RESULT ---
merged_df.to_csv(OUTPUT_FILE, index=False)

print("\n--- Merged Data Head (Duration in Whole Days) ---")
print(merged_df[["Sub T1 No", "DURATIONS (Whole Days)"]].head())
print(f"\n[SUCCESS] Final merged data saved to: {os.path.abspath(OUTPUT_FILE)}")
print("--- Script Finished ---")
