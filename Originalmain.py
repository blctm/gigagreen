import streamlit as st
import pandas as pd
from IO.excel_utils import extract_excel_to_dataframe
from utils.processing import drop_first_row, convert_columns
from kpi.test import calculate_metrics

# Streamlit App
st.title("Electrochemical KPI Summary Generator")

#Initialize session state for storing processing dataframes
if "all_summaries" not in st.session_state:
    st.session_state["all_summaries"] = []  # To store individual summary DataFrames


# File uploader widget
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        #STEP 1
        # Extract data to a DataFrame using the provided utility function
        df = extract_excel_to_dataframe(uploaded_file)
        #Display the raw dataframe
       # st.subheader("Extracted DataFrame")
        #st.dataframe(df)
        #STEP 2: Drop de first row
        df = drop_first_row(df)
        #STEP 3 convert to the right format
        df = convert_columns(df)
        #Display the processed Dataframe
        #st.subheader("Processed Dataframe")
        #st.dataframe(df)
        #STEP 4: calculate metrics
        summary_df = calculate_metrics(df, uploaded_file.name)
        # Add the current summary DataFrame to the session state
        st.session_state["all_summaries"].append(summary_df)
        # Display the summary for the current file
        st.success(f"Processed {uploaded_file.name} successfully!")
        st.subheader(f"Summary for {uploaded_file.name}")
        st.dataframe(summary_df, use_container_width=True)
   
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Combine all summaries if available
if st.session_state["all_summaries"]:
    combined_summary_df = pd.concat(st.session_state["all_summaries"], ignore_index=True)

    # Display the combined summary DataFrame
    st.subheader("Combined Summary for All Files")
    st.dataframe(combined_summary_df, use_container_width=True)

 # Option to download the combined summary
    st.download_button(
        label="Download Combined Summary",
        data=combined_summary_df.to_csv(index=False, sep=',', encoding='utf-8'),
        file_name="combined_kpi_summary.csv",
        mime="text/csv"
        
    )
                     
    
        
