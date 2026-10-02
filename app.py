import streamlit as st
import pandas as pd
import datetime

# Page configuration
st.set_page_config(page_title="Expense Tracker", page_icon="📊", layout="wide")

# Initialize Session State
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Date", "Description", "Category", "Type", "Amount", "Month"])

if 'debts' not in st.session_state:
    st.session_state.debts = pd.DataFrame(columns=["Date", "Person", "Type", "Amount", "Due Date", "Status"])

months_list = ["January", "February", "March", "April", "May", "June", 
               "July", "August", "September", "October", "November", "December"]

categories = ["Groceries", "Rent", "Bills", "Travel", "Food", "Shopping", "Entertainment", "Salary", "Investment", "Others"]

st.title("📊 Financial Dashboard & Expense Tracker")

# Sidebar Navigation
menu = st.sidebar.radio("Navigation", ["Monthly Tracker", "Debt & Loan Records", "Annual Master Dashboard"])

# 1. MONTHLY TRACKER
if menu == "Monthly Tracker":
    st.header("💳 Monthly Budget Transactions")
    
    selected_month = st.sidebar.selectbox("Select Month", months_list)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add Transaction")
        date = st.date_input("Date", datetime.date.today())
        desc = st.text_input("Description")
        cat = st.selectbox("Category", categories)
        trans_type = st.selectbox("Type", ["Income", "Expense"])
        amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
        
        if st.button("Add Transaction"):
            new_data = pd.DataFrame([{
                "Date": str(date),
                "Description": desc,
                "Category": cat,
                "Type": trans_type,
                "Amount": amount,
                "Month": selected_month
            }])
            st.session_state.transactions = pd.concat([st.session_state.transactions, new_data], ignore_index=True)
            st.success("Transaction Added!")

    m_df = st.session_state.transactions[st.session_state.transactions["Month"] == selected_month]

    with col2:
        st.subheader(f"Summary for {selected_month}")
        inc = m_df[m_df["Type"] == "Income"]["Amount"].sum()
        exp = m_df[m_df["Type"] == "Expense"]["Amount"].sum()
        bal = inc - exp
        savings_rate = (bal / inc * 100) if inc > 0 else 0

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Income", f"₹{inc:,.2f}")
        m2.metric("Total Expense", f"₹{exp:,.2f}")
        m3.metric("Net Balance", f"₹{bal:,.2f}")
        m4.metric("Savings Rate", f"{savings_rate:.1f}%")

        st.subheader("Transactions List")
        st.dataframe(m_df[["Date", "Description", "Category", "Type", "Amount"]], use_container_width=True)

    st.divider()
    
    st.subheader("📈 Category Expense Breakdown")
    exp_df = m_df[m_df["Type"] == "Expense"]
    if not exp_df.empty:
        cat_summary = exp_df.groupby("Category")["Amount"].sum().reset_index()
        cat_summary["% Share"] = (cat_summary["Amount"] / exp) * 100
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.dataframe(cat_summary.style.format({"Amount": "₹{:.2f}", "% Share": "{:.1f}%"}), use_container_width=True)
        with c2:
            st.bar_chart(cat_summary.set_index("Category")["Amount"])
    else:
        st.info("No expense data recorded for this month.")

# 2. DEBT & LOAN RECORDS
elif menu == "Debt & Loan Records":
    st.header("🤝 Debt & Loan Records")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add Debt/Loan")
        d_date = st.date_input("Date", datetime.date.today())
        person = st.text_input("Person / Description")
        d_type = st.selectbox("Type", ["Lent (Receivable)", "Borrowed (Payable)"])
        d_amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
        due_date = st.date_input("Due Date", datetime.date.today() + datetime.timedelta(days=30))
        status = st.selectbox("Status", ["Pending", "Clear"])

        if st.button("Save Record"):
            new_debt = pd.DataFrame([{
                "Date": str(d_date),
                "Person": person,
                "Type": d_type,
                "Amount": d_amount,
                "Due Date": str(due_date),
                "Status": status
            }])
            st.session_state.debts = pd.concat([st.session_state.debts, new_debt], ignore_index=True)
            st.success("Record Saved!")

    with col2:
        st.subheader("Overview")
        lent = st.session_state.debts[st.session_state.debts["Type"] == "Lent (Receivable)"]["Amount"].sum()
        borrowed = st.session_state.debts[st.session_state.debts["Type"] == "Borrowed (Payable)"]["Amount"].sum()
        net_pos = lent - borrowed

        d1, d2, d3 = st.columns(3)
        d1.metric("Total Lent (Receivables)", f"₹{lent:,.2f}")
        d2.metric("Total Borrowed (Payables)", f"₹{borrowed:,.2f}")
        d3.metric("Net Position", f"₹{net_pos:,.2f}")

        st.subheader("Records List")
        st.dataframe(st.session_state.debts, use_container_width=True)

# 3. ANNUAL MASTER DASHBOARD
elif menu == "Annual Master Dashboard":
    st.header("📊 Annual Master Financial Dashboard")

    df = st.session_state.transactions
    
    total_inc = df[df["Type"] == "Income"]["Amount"].sum()
    total_exp = df[df["Type"] == "Expense"]["Amount"].sum()
    net_savings = total_inc - total_exp
    savings_rate = (net_savings / total_inc * 100) if total_inc > 0 else 0

    lent = st.session_state.debts[st.session_state.debts["Type"] == "Lent (Receivable)"]["Amount"].sum()
    borrowed = st.session_state.debts[st.session_state.debts["Type"] == "Borrowed (Payable)"]["Amount"].sum()

    a1, a2, a3, a4, a5, a6 = st.columns(6)
    a1.metric("Annual Income", f"₹{total_inc:,.2f}")
    a2.metric("Annual Expense", f"₹{total_exp:,.2f}")
    a3.metric("Net Savings", f"₹{net_savings:,.2f}")
    a4.metric("Savings Rate", f"{savings_rate:.1f}%")
    a5.metric("Total Lent", f"₹{lent:,.2f}")
    a6.metric("Total Borrowed", f"₹{borrowed:,.2f}")

    st.divider()

    st.subheader("Month-wise Breakdown")
    monthly_data = []
    for m in months_list:
        m_trans = df[df["Month"] == m]
        inc = m_trans[m_trans["Type"] == "Income"]["Amount"].sum()
        exp = m_trans[m_trans["Type"] == "Expense"]["Amount"].sum()
        monthly_data.append({
            "Month": m,
            "Income (₹)": inc,
            "Expense (₹)": exp,
            "Net Balance (₹)": inc - exp
        })

    annual_summary_df = pd.DataFrame(monthly_data)
    st.dataframe(annual_summary_df, use_container_width=True)

    if not df.empty:
        st.subheader("Income vs Expenses Trend")
        st.line_chart(annual_summary_df.set_index("Month")[["Income (₹)", "Expense (₹)"]])