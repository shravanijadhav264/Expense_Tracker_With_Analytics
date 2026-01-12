# Expense Tracker with Analytics

A simple expense tracker built with Python, SQLite, and Streamlit that allows users to log income and expenses, view category-wise and monthly analytics, and manage personal finances effectively.

---

## Features

- Add, view, and categorize income and expenses
- View total income, total expenses, and category-wise breakdown
- Monthly expense summary
- **Analytics** handled via `analytics.py` (currently placeholder for future report generation)
- **Structured data models** in `models.py` (currently placeholder)
- Data stored in SQLite via `database.py`
- Streamlit-based interactive web interface

## Project Structure

Expense_Tracker_With_Analytics/
├── app.py # Streamlit frontend
├── database.py # SQLite database connection and CRUD operations
├── analytics.py # Placeholder: functions for generating reports
├── models.py # Placeholder: data models / classes
├── requirements.txt # Python dependencies
├── README.md # Project documentation
├── screenshots/
│ └── app_screenshot.png
└── .gitignore # Exclude venv, .env, cache files

## Future Improvements

- Fill `analytics.py` with category-wise, monthly, and yearly charts
- Add methods in `models.py` for structured expense objects
- Implement delete/update functionality in the UI
- Export expense reports as PDF
 
