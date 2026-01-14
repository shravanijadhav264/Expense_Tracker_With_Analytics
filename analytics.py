import matplotlib.pyplot as plt
import pandas as pd

def plot_category_expenses(df):
    plt.figure(figsize=(6,4))
    if not df.empty:
        df_grouped = df.groupby('category')['amount'].sum().reset_index()
        plt.bar(df_grouped['category'], df_grouped['amount'], color='skyblue')
        plt.title("Category-wise Expenses")
        plt.ylabel("Amount")
        plt.xticks(rotation=45, ha='right')
    else:
        plt.text(0.5, 0.5, 'No Data', ha='center', va='center')
    plt.tight_layout()
    return plt

def plot_monthly_expenses(df):
    plt.figure(figsize=(6,4))
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        df_grouped = df.groupby('month')['amount'].sum().reset_index()
        plt.bar(df_grouped['month'].astype(str), df_grouped['amount'], color='lightgreen')
        plt.title("Monthly Expenses")
        plt.ylabel("Amount")
        plt.xticks(rotation=45, ha='right')
    else:
        plt.text(0.5, 0.5, 'No Data', ha='center', va='center')
    plt.tight_layout()
    return plt
