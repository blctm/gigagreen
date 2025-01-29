import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# SharePoint Base Information
BASE_SHAREPOINT_URL = "https://politoit.sharepoint.com/_api/web/GetFolderByServerRelativeUrl('/teams/PRJ_GIGAGREEN/Documenti_condivisi/General/WP2_Design_for_Manufacturing/Digital_Twins/Electrochemical_raw_data')/Files"

# Function to list files dynamically from SharePoint
def list_files():
    headers = {"Accept": "application/json;odata=verbose"}
    try:
        response = requests.get(BASE_SHAREPOINT_URL, headers=headers, cookies=requests.utils.dict_from_cookiejar(requests.get(BASE_SHAREPOINT_URL).cookies))
        if response.status_code == 200:
            files_data = response.json()["d"]["results"]
            return [file["Name"] for file in files_data]
        else:
            st.error(f"Failed to fetch file list from SharePoint. HTTP Status: {response.status_code}")
            st.write("Response Text:", response.text)
            return []
    except Exception as e:
        st.error(f"Error accessing SharePoint: {e}")
        return []

# Function to process the Excel file
def calculate_metrics(df, filename):
    try:
        first_discharge = df.iloc[0]['Discharge Capacity']
        first_charge = df.iloc[0]['Charge Capacity']
        first_coulombic_efficiency = (first_charge / first_discharge) * 100
        third_lithiation = df.iloc[2]['Discharge Capacity']
        
        # Calculating averages
        Avg_C5 = df.loc[3:7, 'Discharge Capacity'].mean()
        Avg_C2 = df.loc[8:12, 'Discharge Capacity'].mean()
        Avg_1C = df.loc[13:17, 'Discharge Capacity'].mean()
        Avg_2C = df.loc[18:22, 'Discharge Capacity'].mean()
        Avg_1CR = df.loc[23:101, 'Discharge Capacity'].mean()
        last_lithiation = df.iloc[102]['Discharge Capacity']
        
        # Extracting cell ID
        cell_id = filename.replace(".xlsx", "")
        anodo = cell_id.split("_")[0]
        
        # Creating DataFrame
        summary = {
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
        
        return pd.DataFrame([summary])
    
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None

# Streamlit UI
st.title("📊 Electrochemical KPI Processor")
st.write("Browse SharePoint folders and select files for processing.")

# Fetch list of files dynamically
files = list_files()
if files:
    selected_files = st.multiselect("Choose files to process:", files)

    # Process button
    if st.button("Process Selected Files"):
        if not selected_files:
            st.warning("⚠ Please select at least one file.")
        else:
            summaries = []
            for file in selected_files:
                file_url = f"https://politoit.sharepoint.com/_layouts/15/download.aspx?sourceurl=/teams/PRJ_GIGAGREEN/Documenti%2520condivisi/General/WP2%2520Design%2520for%2520Manufacturing/Digital%2520Twins/Electrochemical_raw_data/{file}"
                try:
                    response = requests.get(file_url)
                    if response.status_code == 200:
                        df = pd.read_excel(BytesIO(response.content), engine="openpyxl")
                        st.success(f"✅ File {file} downloaded successfully")
                        summary_df = calculate_metrics(df, file)
                        if summary_df is not None:
                            summaries.append(summary_df)
                    else:
                        st.error(f"⚠ Failed to download {file}. HTTP Status: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Error loading file: {e}")
            
            if summaries:
                final_df = pd.concat(summaries, ignore_index=True)
                st.write("📊 **Processed Data Summary:**")
                st.dataframe(final_df)
else:
    st.warning("No files found in the SharePoint folder.")

# Manual file upload fallback
st.write("---")
st.write("If SharePoint access fails, upload your files manually:")
manual_upload = st.file_uploader("Upload Excel files", accept_multiple_files=True, type=["xlsx"])

if manual_upload:
    summaries = []
    for uploaded_file in manual_upload:
        try:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
            summary_df = calculate_metrics(df, uploaded_file.name)
            if summary_df is not None:
                summaries.append(summary_df)
        except Exception as e:
            st.error(f"Error processing uploaded file {uploaded_file.name}: {e}")
    
    if summaries:
        final_df = pd.concat(summaries, ignore_index=True)
        st.write("📊 **Processed Data Summary from Uploaded Files:**")
        st.dataframe(final_df)

