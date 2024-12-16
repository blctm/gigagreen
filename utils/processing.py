def drop_first_row(df):
    """
    Drops the first row of the DataFrame (after the header).
    
    Parameters:
    df (pd.DataFrame): Input DataFrame.

    Returns:
    pd.DataFrame: DataFrame with the first row removed.
    """
    return df.iloc[1:].reset_index(drop=True)

def convert_columns(df):
    """
    Converts the first column to integer and the remaining columns to float.

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with converted column types.
    """
    df['Cycle Number'] = df['Cycle Number'].astype(int)
    df['Charge Capacity']= df['Charge Capacity'].astype(float)
    df['Discharge Capacity'] = df['Discharge Capacity'].astype(float)
    df['Current'] = df['Current'].astype(float)
    df['Coulombic Efficiency'] = df['Coulombic Efficiency'].astype(float)

    return df