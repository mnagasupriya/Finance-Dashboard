import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Finance Dashboard", layout="wide")


DATA_FILE = "transactions.csv"

# -----------------------------
# Load Data
# -----------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame([
            {"Date": "2026-03-01", "Amount": 5000, "Category": "Salary", "Type": "Income"},
            {"Date": "2026-03-03", "Amount": 2000, "Category": "Freelance", "Type": "Income"},
            {"Date": "2026-03-05", "Amount": 1500, "Category": "Food", "Type": "Expense"},
            {"Date": "2026-03-07", "Amount": 800, "Category": "Transport", "Type": "Expense"},
            {"Date": "2026-03-10", "Amount": 1200, "Category": "Shopping", "Type": "Expense"},
        ])
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# -----------------------------
# Session State
# -----------------------------
if "data" not in st.session_state:
    st.session_state.data = load_data()

if "role" not in st.session_state:
    st.session_state.role = "Viewer"

df = st.session_state.data.copy()

if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Settings")

st.session_state.role = st.sidebar.selectbox(
    "Select Role", ["Viewer", "Admin"]
)

# -----------------------------
# Helper
# -----------------------------
def calculate_summary(df):
    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()
    return income, expense, income - expense

# -----------------------------
# Header
# -----------------------------
st.title("Finance Dashboard")

# -----------------------------
# Summary
# -----------------------------
income, expense, balance = calculate_summary(df)

col1, col2, col3 = st.columns(3)
col1.metric("Total Balance", f"₹{balance}")
col2.metric("Total Income", f"₹{income}")
col3.metric("Total Expense", f"₹{expense}")

st.markdown("---")

# -----------------------------
# Charts
# -----------------------------
st.subheader("Analytics")

# Make line chart full width (bigger)
df_sorted = df.sort_values("Date").copy()
df_sorted["Signed"] = df_sorted.apply(
    lambda x: x["Amount"] if x["Type"] == "Income" else -x["Amount"], axis=1
)
df_sorted["Balance"] = df_sorted["Signed"].cumsum()

fig_line = px.line(df_sorted, x="Date", y="Balance", title="Balance Trend")
st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")

# Pie Charts Section

col1, col2 = st.columns(2)

income_df = df[df["Type"] == "Income"]
expense_df = df[df["Type"] == "Expense"]

# Income Pie
with col1:
    st.markdown("### Income Breakdown")
    if not income_df.empty:
        fig_income = px.pie(
            income_df,
            names="Category",
            values="Amount"
        )
        st.plotly_chart(fig_income, use_container_width=True)
    else:
        st.info("No income data available")

# Expense Pie
with col2:
    st.markdown("### Expense Breakdown")
    if not expense_df.empty:
        fig_expense = px.pie(
            expense_df,
            names="Category",
            values="Amount"
        )
        st.plotly_chart(fig_expense, use_container_width=True)
    else:
        st.info("No expense data available")
st.markdown("---")
# -----------------------------
# Transactions
# -----------------------------
st.subheader("Transactions")

search = st.text_input("Search Category")
filter_type = st.selectbox("Filter Type", ["All", "Income", "Expense"])
sort_by = st.selectbox("Sort By", ["Date", "Amount"])

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[filtered_df["Category"].str.contains(search, case=False)]

if filter_type != "All":
    filtered_df = filtered_df[filtered_df["Type"] == filter_type]

filtered_df = filtered_df.sort_values(by=sort_by).reset_index()

if filtered_df.empty:
    st.warning("No transactions found")
else:
    header = st.columns([1, 2, 2, 2, 2, 3])
    header[0].write("Index")
    header[1].write("Date")
    header[2].write("Amount")
    header[3].write("Category")
    header[4].write("Type")
    header[5].write("Actions")

    st.markdown("---")

    for _, row in filtered_df.iterrows():
        cols = st.columns([1, 2, 2, 2, 2, 3])

        cols[0].write(row["index"])
        cols[1].write(row["Date"].date() if pd.notnull(row["Date"]) else "-")
        cols[2].write(f"₹{row['Amount']}")
        cols[3].write(row["Category"])
        cols[4].write(row["Type"])

        # Side-by-side buttons
        action_cols = cols[5].columns(2)

        if st.session_state.role == "Admin":
            if action_cols[0].button("Edit", key=f"edit_{row['index']}"):
                st.session_state.edit_index = row["index"]

            if action_cols[1].button("Delete", key=f"delete_{row['index']}"):
                st.session_state.delete_index = row["index"]
        else:
            action_cols[0].button("Edit", disabled=True, key=f"edit_dis_{row['index']}")
            action_cols[1].button("Delete", disabled=True, key=f"del_dis_{row['index']}")

# -----------------------------
# Edit
# -----------------------------
if "edit_index" in st.session_state:
    st.subheader("Edit Transaction")

    row = df.loc[st.session_state.edit_index]

    with st.form("edit_form"):
        date = st.date_input("Date", row["Date"])
        amount = st.number_input("Amount", value=int(row["Amount"]))
        category = st.text_input("Category", value=row["Category"])
        t_type = st.selectbox(
            "Type",
            ["Income", "Expense"],
            index=0 if row["Type"] == "Income" else 1
        )

        if st.form_submit_button("Update"):
            df.loc[st.session_state.edit_index] = [date, amount, category, t_type]
            st.session_state.data = df
            save_data(df)
            del st.session_state.edit_index
            st.success("Updated successfully")
            st.rerun()

# -----------------------------
# Delete Confirm
# -----------------------------
if "delete_index" in st.session_state:
    st.warning("Are you sure you want to delete this transaction?")

    col1, col2 = st.columns(2)

    if col1.button("Yes"):
        st.session_state.data = df.drop(st.session_state.delete_index).reset_index(drop=True)
        save_data(st.session_state.data)
        del st.session_state.delete_index
        st.success("Deleted successfully")
        st.rerun()

    if col2.button("Cancel"):
        del st.session_state.delete_index

st.markdown("---")

# -----------------------------
# Add
# -----------------------------
if st.session_state.role == "Admin":
    st.subheader("Add Transaction")

    with st.form("add_form", clear_on_submit=True):
        date = st.date_input("Date")
        amount = st.number_input("Amount", min_value=0)
        category = st.text_input("Category")
        t_type = st.selectbox("Type", ["Income", "Expense"])

        if st.form_submit_button("Add"):
            if amount <= 0 or category.strip() == "":
                st.error("Invalid input")
            else:
                new_row = pd.DataFrame([{
                    "Date": pd.to_datetime(date),
                    "Amount": amount,
                    "Category": category,
                    "Type": t_type
                }])

                st.session_state.data = pd.concat(
                    [st.session_state.data, new_row],
                    ignore_index=True
                )

                save_data(st.session_state.data)
                st.success("Transaction added")
                st.rerun()

st.markdown("---")

# -----------------------------
# Insights
# -----------------------------
st.subheader("Insights")

if not expense_df.empty:
    top_category = expense_df.groupby("Category")["Amount"].sum().idxmax()
    avg_expense = expense_df["Amount"].mean()

    st.write(f"Highest Spending Category: {top_category}")
    st.write(f"Average Expense: ₹{round(avg_expense, 2)}")

if income > expense:
    st.success("You are saving money")
else:
    st.warning("Expenses are higher than income")

monthly = df.dropna(subset=["Date"]).groupby(df["Date"].dt.month)["Amount"].sum()

if not monthly.empty:
    st.bar_chart(monthly)

# -----------------------------
# Export
# -----------------------------
# -----------------------------
# Export (Final Clean Report)
# -----------------------------
from datetime import datetime

def generate_report(df):
    df_export = df.copy()

    # Format Date column
    df_export["Date"] = df_export["Date"].dt.strftime("%Y-%m-%d")

    # Calculate summary
    income = df_export[df_export["Type"] == "Income"]["Amount"].sum()
    expense = df_export[df_export["Type"] == "Expense"]["Amount"].sum()
    balance = income - expense

    # Current date & time
    current_time = datetime.now().strftime("%d %b %Y, %I:%M %p")

    # Unified columns
    columns = ["Section", "Details", "Amount", "Category", "Type"]

    # -----------------------------
    # Description Section
    # -----------------------------
    description = [
        ["Report", "Finance Dashboard Report", "", "", ""],
        ["Report", f"Generated on: {current_time}", "", "", ""],
        ["Report", "Provides an overview of financial transactions.", "", "", ""],
        ["Report", "Includes income, expenses, and balance analysis.", "", "", ""],
        ["", "", "", "", ""]
    ]

    # -----------------------------
    # Summary Section
    # -----------------------------
    summary = [
        ["Summary", "Total Income", income, "", ""],
        ["Summary", "Total Expense", expense, "", ""],
        ["Summary", "Net Balance", balance, "", ""],
        ["", "", "", "", ""]
    ]

    # -----------------------------
    # Transactions Section
    # -----------------------------
    transactions = [
        ["Transaction", row["Date"], row["Amount"], row["Category"], row["Type"]]
        for _, row in df_export.iterrows()
    ]

    # Combine all sections
    final_df = pd.DataFrame(
        description + summary + transactions,
        columns=columns
    )

    return final_df


# Generate report
report_df = generate_report(st.session_state.data)

# Convert to CSV
csv = report_df.to_csv(index=False).encode("utf-8")

# Download button
st.download_button(
    label="Download Report",
    data=csv,
    file_name="finance_report.csv",
    mime="text/csv"
)
