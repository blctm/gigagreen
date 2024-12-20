import os
import pandas as pd

def calculate_metrics(df, filename):
    """
    Calculates various electrochemical metrics and returns a summary DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame with electrochemical data, containing 'Discharge Capacity' and 'Charge Capacity' columns.
    filename (str): Name of the file being processed.

    Returns:
    pd.DataFrame: A DataFrame summarizing the calculated metrics.
    """
    # Extracting necessary values from the DataFrame
    first_discharge = df.iloc[0]['Discharge Capacity']
    first_charge = df.iloc[0]['Charge Capacity']
    first_coulombic_efficiency = (first_charge / first_discharge) * 100
    third_lithiation = df.iloc[2]['Discharge Capacity']

    # Calculating averages over specified ranges
    Avg_C5 = df.loc[3:7, 'Discharge Capacity'].mean()
    Avg_C2 = df.loc[8:12, 'Discharge Capacity'].mean()
    Avg_1C = df.loc[13:17, 'Discharge Capacity'].mean()
    Avg_2C = df.loc[18:22, 'Discharge Capacity'].mean()
    Avg_1CR = df.loc[23:101, 'Discharge Capacity'].mean()

    # Extracting the last lithiation capacity
    last_lithiation = df.iloc[102]['Discharge Capacity']

    # Extracting the cell ID from the filename
    cell_id = os.path.splitext(filename)[0]
    anodo = cell_id.split("_")[0]  # Extract characters before the first underscore

    # Creating a dictionary of calculated metrics
    final = {
        "cell_id": cell_id,
        "Anodo": anodo,
        "1st lithiation capacity (mAh/g)": first_discharge,
        "1st coulombic efficiency (%)": first_coulombic_efficiency,
        "3rd lithiation capacity (mAh/g)": third_lithiation,
        "average capacity@C/5 (mAh/g)": Avg_C5,
        "average capacity@C/2 (mAh/g)": Avg_C2,
        "average capacity@1C (mAh/g)": Avg_1C,
        "average capacity@1Cch-2Cdch (mAh/g)": Avg_2C,
        "average capacity@1CR (mAh/g)": Avg_1CR,
        "103rd capacity": last_lithiation
    }

    # Convert the dictionary to a DataFrame
    df_summary = pd.DataFrame([final])

    return df_summary
