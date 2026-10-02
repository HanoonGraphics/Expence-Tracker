import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Expense Tracker", page_icon="📊", layout="wide")

# Google Sheet CSV Link
SHEET_ID = "1rHNLc_oNVJD4hrKS179aZ0sq2eZm-BQ2MJ5dEKgb7ao"
SHEET_NAME = "Transactions"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

st.title("📊 Financial Dashboard & Expense Tracker")

# Function to load data from Google Sheets
@st.cache_data(ttl=5) # 5 സെക്കൻഡിൽ സ്വയം അപ്‌ഡേറ്റ് ചെയ്യും
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        return pd.DataFrame()

# Data load ചെയ്യുന്നു
df = load_data()

# Navigation menu
menu = st.sidebar.radio("Navigation", ["Monthly Tracker", "Debt & Loan Records", "Annual Master Dashboard"])

if menu == "Monthly Tracker":
    st.subheader("Monthly Expense & Income")
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Google Sheet-ൽ നിന്ന് ഡാറ്റ കാണാൻ സാധിക്കുന്നില്ല. ഷീറ്റിന്റെ Share Settings 'Anyone with link' എന്ന് മാറ്റിയിട്ടുണ്ടെന്ന് ഉറപ്പുവരുത്തുക.")

    st.info("💡 ഗൂഗിൾ ഷീറ്റിൽ എൻട്രികൾ ആഡ് ചെയ്താൽ ഇവിടെ തത്സമയം ഫോണിലും സിസ്റ്റത്തിലും ഒരുപോലെ കാണാൻ സാധിക്കും!")
