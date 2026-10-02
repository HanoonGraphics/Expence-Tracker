import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Expense Tracker", page_icon="📊", layout="wide")

st.title("📊 Financial Dashboard & Expense Tracker")

# Google Sheet Direct Export Link
sheet_url = "https://docs.google.com/spreadsheets/d/1rHNLc_oNVJD4hrKS179aZ0sq2eZm-BQ2MJ5dEKgb7ao/export?format=csv"

@st.cache_data(ttl=2)
def load_data():
    try:
        # direct csv load
        data = pd.read_csv(sheet_url)
        return data
    except Exception as e:
        st.error(f"Error loading sheet: {e}")
        return pd.DataFrame()

df = load_data()

# Navigation menu
menu = st.sidebar.radio("Navigation", ["Monthly Tracker", "Debt & Loan Records", "Annual Master Dashboard"])

if menu == "Monthly Tracker":
    st.subheader("Monthly Expense & Income")
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Google Sheet-ൽ നിന്ന് ഡാറ്റ കാണാൻ സാധിക്കുന്നില്ല. ഗൂഗിൾ ഷീറ്റിൽ ഡാറ്റ നൽകിയിട്ടുണ്ടെന്ന് ഉറപ്പുവരുത്തുക.")
