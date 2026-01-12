# analytics.py
import matplotlib.pyplot as plt
import pandas as pd

def plot_category_expenses(df):
    # df = DataFrame with 'category' and 'amount' columns
    cat_summary = df.groupby('category')['amount'].sum()
    fig, ax = plt.subplots()
    ax.pie(cat_summary, labels=cat_summary.index, autopct='%1.1f%%')
    return fig

def plot_monthly_expenses(df):
    # df = DataFrame with 'date' and 'amount' columns
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    month_summary = df.groupby('month')['amount'].sum()
    fig, ax = plt.subplots()
    month_summary.plot(kind='bar', ax=ax)
    ax.set_ylabel("Total Expense")
    return fig
