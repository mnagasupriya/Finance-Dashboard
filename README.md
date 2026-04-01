# Finance-Dashboard
Streamlit-based finance dashboard for tracking expenses, analyzing trends, and generating reports.

## Overview

This project is a simple and interactive Finance Dashboard built using Streamlit.
It allows users to track financial transactions, analyze spending patterns, and view insights through visualizations.

The application focuses on clean UI design, proper state management, and role-based interaction.

---

## Features

### Dashboard Overview

* Displays Total Balance, Income, and Expenses
* Balance trend visualization (line chart)
* Category-wise breakdown (income & expense pie charts)

### Transactions Management

* View all transactions (Date, Amount, Category, Type)
* Search, filter, and sort functionality
* Add new transactions (Admin only)
* Edit existing transactions
* Delete transactions with confirmation

### Role-Based Access

* Viewer: Read-only access
* Admin: Full control (Add/Edit/Delete)

### Insights

* Highest spending category
* Average expense
* Monthly overview chart
* Income vs Expense comparison

### Export Functionality

* Download report as CSV
* Includes:

  * Description
  * Generated date & time
  * Summary (Income, Expense, Balance)
  * Transaction data

---

## Tech Stack

* Python
* Streamlit
* Pandas
* Plotly

---

## How to Run

1. Install dependencies:

```
pip install streamlit pandas plotly
```

2. Run the app:

```
streamlit run app.py
```

---

## Project Structure

```
project-folder/
│
├── app.py
├── transactions.csv
└── README.md
```

---

## Approach

* Used Streamlit for rapid UI development
* Managed state using session_state
* Structured UI into sections: Dashboard, Transactions, Insights
* Ensured responsiveness and clean layout
* Focused on usability and clarity over complexity

---

## Future Improvements

* Excel/PDF export
* Advanced filters
* User authentication
* Database integration
* AI intigration
  

---

## Conclusion

This project demonstrates frontend thinking, UI design, and data handling using a simple and effective approach.

