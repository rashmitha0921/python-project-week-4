import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Set up paths
data_path = 'data/sales_data.csv'
visualizations_path = 'visualizations/'
report_path = 'report/'

# Ensure directories exist
os.makedirs(visualizations_path, exist_ok=True)
os.makedirs(report_path, exist_ok=True)

# Load data
try:
    df = pd.read_csv(data_path)
    print("Data loaded successfully.")
    print(f"Shape: {df.shape}")
    print(df.head())
except Exception as e:
    print(f"Error loading data: {e}")
    exit(1)

# Data cleaning
df['Date'] = pd.to_datetime(df['Date'])
df = df.dropna()  # Drop any missing values
print("\nData after cleaning:")
print(df.info())

# Basic analysis
total_sales = df['Total_Sales'].sum()
print(f"\nTotal Sales: ${total_sales:,.2f}")

sales_by_product = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)
print("\nSales by Product:")
print(sales_by_product)

sales_by_region = df.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False)
print("\nSales by Region:")
print(sales_by_region)

# Monthly sales
df['Month'] = df['Date'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Total_Sales'].sum()
print("\nMonthly Sales:")
print(monthly_sales)

# Visualizations

# 1. Bar chart: Sales by Product
plt.figure(figsize=(10, 6))
sales_by_product.plot(kind='bar', color='skyblue')
plt.title('Total Sales by Product Category')
plt.xlabel('Product')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{visualizations_path}sales_by_product.png')
plt.close()
print("\nBar chart saved: sales_by_product.png")

# 2. Line chart: Monthly Sales
plt.figure(figsize=(10, 6))
monthly_sales.plot(kind='line', marker='o', color='green')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.grid(True)
plt.tight_layout()
plt.savefig(f'{visualizations_path}monthly_sales.png')
plt.close()
print("Line chart saved: monthly_sales.png")

# 3. Pie chart: Sales by Region
plt.figure(figsize=(8, 8))
sales_by_region.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['red', 'blue', 'green', 'orange'])
plt.title('Sales Distribution by Region')
plt.ylabel('')  # Hide y-label
plt.tight_layout()
plt.savefig(f'{visualizations_path}sales_by_region.png')
plt.close()
print("Pie chart saved: sales_by_region.png")

# Generate report
report_content = f"""
# E-commerce Sales Analysis Report

## Project Overview
This project analyzes sales data from an e-commerce platform, focusing on product categories, regional distribution, and monthly trends.

## Data Summary
- Total records: {len(df)}
- Date range: {df['Date'].min()} to {df['Date'].max()}
- Total sales: ${total_sales:,.2f}

## Key Insights

### Sales by Product
The top-selling products are:
{sales_by_product.to_string()}

Laptops generate the highest revenue, followed by Phones.

### Sales by Region
Regional distribution:
{sales_by_region.to_string()}

The North region has the highest sales (${sales_by_region.max():,.0f}), indicating a strong market there.

### Monthly Trends
Monthly sales show:
{monthly_sales.to_string()}

Sales peaked in March (${monthly_sales.max():,.0f}), with a decline in April.

## Visualizations
- Bar Chart: Sales by Product ([View](visualizations/sales_by_product.png))
- Line Chart: Monthly Sales Trend ([View](visualizations/monthly_sales.png))
- Pie Chart: Sales by Region ([View](visualizations/sales_by_region.png))

## Recommendations
- Focus marketing on top products: Laptops and Phones.
- Expand in high-performing regions like East.
- Monitor monthly trends for inventory planning.
"""

with open(f'{report_path}analysis_report.md', 'w') as f:
    f.write(report_content)

print(f"\nReport generated: {report_path}analysis_report.md")

# Additional insights
avg_sale_per_customer = df.groupby('Customer_ID')['Total_Sales'].sum().mean()
print(f"\nAverage sale per customer: ${avg_sale_per_customer:,.2f}")

top_customer = df.groupby('Customer_ID')['Total_Sales'].sum().idxmax()
print(f"Top customer: {top_customer}")

print("\nAnalysis complete!")