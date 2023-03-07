#!/usr/bin/env python
# coding: utf-8

# # Sales Analysis

# In[2]:


import pandas as pd
import numpy as np
import seaborn as sns
import datetime 
import matplotlib.pyplot as plt


# In[3]:


# Import all monthl files into Jupyter Notebook

file_location = 'C:\\Users\\ragir\\OneDrive\\Desktop\\DATA ANALYTICS\\Portfolio Projects\\Sales Analysis\\'

df1 = pd.read_excel(file_location + 'Sales_January_2019.xlsx')
df2 = pd.read_excel(file_location + 'Sales_February_2019.xlsx')
df3 = pd.read_excel(file_location + 'Sales_March_2019.xlsx')
df4 = pd.read_excel(file_location + 'Sales_April_2019.xlsx')
df5 = pd.read_excel(file_location + 'Sales_May_2019.xlsx')
df6 = pd.read_excel(file_location + 'Sales_June_2019.xlsx')
df7 = pd.read_excel(file_location + 'Sales_July_2019.xlsx')
df8 = pd.read_excel(file_location + 'Sales_August_2019.xlsx')
df9 = pd.read_excel(file_location + 'Sales_September_2019.xlsx')
df10 = pd.read_excel(file_location + 'Sales_October_2019.xlsx')
df11 = pd.read_excel(file_location + 'Sales_November_2019.xlsx')
df12 = pd.read_excel(file_location + 'Sales_December_2019.xlsx')


# In[4]:


# Merging all the data

sales_data = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12], axis=0, ignore_index=True)


# In[5]:


# View the top 5 of the merged data

sales_data.head()


# In[6]:


# View the bottom 5 of the merged data

sales_data.tail()


# In[7]:


# Check data info, data types

sales_data.info()


# In[8]:


# Check for NULL rows

sales_data.isnull().sum()


# In[9]:


# Drop all NULLs from dataframe

sales_data.dropna(inplace=True)


# In[10]:


# Check for NULL rows
sales_data.isnull().sum()


# In[11]:


# Check for rows that have column titles as sales data

sales_data[sales_data['Order ID'] == 'Order ID']


# In[12]:


# Get the index of the rows with column titles
index_names = sales_data[sales_data['Order ID'] == 'Order ID'].index

# Drop the rows
sales_data.drop(index_names, inplace=True)


# In[13]:


# Change order ID, Quantity Ordered, Price Each, Order Date columns datatype

sales_data['Order ID'] = sales_data['Order ID'].astype('int64')
sales_data['Quantity Ordered'] = sales_data['Quantity Ordered'].astype('int64')
sales_data['Price Each'] = sales_data['Price Each'].astype('float')
sales_data['Order Date'] = sales_data['Order Date'].astype('datetime64')


# In[14]:


# Check data info, data types

sales_data.info()


# In[15]:


sales_data.head()


# In[17]:


# Create new column for total price (Quantity Ordered * Price Each)

sales_data['Sales'] = sales_data['Quantity Ordered'] * sales_data['Price Each']


# In[18]:


sales_data.head()


# In[23]:


# Create a new column for day of week from the Order Date column

sales_data['Day_of_Week'] = sales_data['Order Date'].dt.day_name()
sales_data.Day_of_Week.head()


# In[24]:


# Create a new column for day of week from the Order Date column

sales_data['Month'] = sales_data['Order Date'].dt.month
sales_data.Month.head()


# In[25]:


sales_data.head()


# In[26]:


# Create a new column for city from the Purchase Address column

sales_data['City'] = sales_data['Purchase Address'].apply(lambda x: x.split(',')[1])


# In[27]:


sales_data.head()


# In[28]:


sales_data.tail()


# In[29]:


sales_data.info()


# In[30]:


# Convert Day_of_Week and Month_Name into categorical datatype

sales_data['Day_of_Week'] = sales_data['Day_of_Week'].astype('category')
sales_data['Month'] = sales_data['Month'].astype('category')
sales_data.info()


# In[31]:


# Check for duplicate values in the dataset
# Check for duplicate Order IDs
duplicate_order_ids = sales_data[sales_data['Order ID'].duplicated()]

if duplicate_order_ids.empty:
    print("There are no duplicate Order IDs.")
else:
    print("Duplicate Order IDs:")
    print(duplicate_order_ids)


# In[32]:


# Drop the duplicate data

sales_data.drop_duplicates(subset='Order ID', inplace=True)


# In[33]:


sales_data.shape


# # Data Exploration

# #### What are the total Orders from January to December and Sales?

# In[34]:



total_orders = sales_data['Order ID'].count()
sum_of_sales = sales_data['Sales'].sum()

print(total_orders)
print(sum_of_sales)


# #### How many Product types were sold?

# In[35]:


product_count = sales_data['Product'].nunique()

product_name = sales_data['Product'].unique()

print(product_count)
print(product_name)


# #### What is the monthly breakdown for the total orders and sales

# In[36]:



sales_data.groupby('Month').agg({'Order ID':'count', 'Sales':'sum'})


# #### Plot to show monthly distribution of the orders and sales

# In[37]:


months = range(1,13)
print(months)

plt.bar(months,sales_data.groupby(['Month']).sum()['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.ticklabel_format(style = 'plain')
plt.show()


# #### What City sold the most product?

# In[38]:


sales_data.groupby('City').agg({'Order ID':'count', 'Sales':'sum'})


# In[39]:



keys = [city for city, df in sales_data.groupby(['City'])]

plt.bar(keys,sales_data.groupby(['City']).sum()['Sales'])
plt.ylabel('Sales in USD ($)')
plt.xlabel('City')
plt.xticks(keys, rotation='vertical', size=8)
plt.ticklabel_format(style = 'plain', axis = 'y')

plt.show()


# #### How do sales perform throughout the hours of the day?

# In[40]:


# Add hour column in the dataframe from the Order Date Column
sales_data['Hour'] = pd.to_datetime(sales_data['Order Date']).dt.hour
sales_data['Minute'] = pd.to_datetime(sales_data['Order Date']).dt.minute
sales_data['Count'] = 1
sales_data.head()


# In[41]:


# Show sales distribution before 
# Group data by Order Hour and count unique Order ID
hourly_orders = sales_data.groupby('Hour')['Order ID'].nunique()

# Create line plot
plt.plot(hourly_orders.index, hourly_orders.values)
plt.xlabel('Hour')
plt.ylabel('Count of Order ID')
plt.title('Distribution of Order ID Count Through Hours')
plt.xticks(range(24))
plt.show()


# The best time to market products through advertisements and promotions would be when the orders are steadily increasing, to take maximize on the already increasing order numbers,so between 0900 hours to 1200 hours and between 1700 hours to 1900 hours 


# #### What was the total orders versus total sales per Product?

# In[74]:


# Calculate total orders (Order IDs) per Product throughout the year

sales_per_item = sales_data.groupby('Product')['Order ID'].count()
sales_per_item = sales_per_item.sort_index()
sales_per_item


# In[75]:


# Calculate total sales per Product throughout the year

sales_per_item = sales_data.groupby('Product')['Sales'].sum()
sales_per_item = sales_per_item.sort_index()
sales_per_item


# #### Plot to show total orders versus total sales per Product

# In[80]:


# Plot a combined bar and line graph to show total orders versus total sales per Product

sales_per_item = sales_data.groupby('Product')['Order ID'].count()
sales_per_item = sales_per_item.sort_index()

sales_per_item_sales = sales_data.groupby('Product')['Sales'].sum()
sales_per_item_sales = sales_per_item_sales.sort_index()

fig, ax = plt.subplots(figsize=(12, 8))

ax.bar(sales_per_item_sales.index, sales_per_item_sales.values, color='b', label='Total Sales')
ax2 = ax.twinx()
ax2.plot(sales_per_item.index, sales_per_item.values, color='r', label='Number of Orders')

ax.set_xlabel('Product')
ax.set_ylabel('Total Sales')
ax2.set_ylabel('Number of Orders')

# plt.xticks(rotation=90)
plt.ticklabel_format(style = 'plain', axis = 'y')
plt.tight_layout()
plt.setp(ax.get_xticklabels(), rotation = 30, horizontalalignment='right', fontsize='small')


plt.show()


# #### How does price compare with the total order and total sales generated from each Product?

# In[83]:


sales_per_item = sales_data.groupby('Product')['Price Each'].unique()
sales_per_item = sales_per_item.sort_index()

sales_per_item_sales = sales_data.groupby('Product')['Sales'].sum()
sales_per_item_sales = sales_per_item_sales.sort_index()

fig, ax = plt.subplots(figsize=(12, 8))

ax.bar(sales_per_item_sales.index, sales_per_item_sales.values, color='b', label='Total Sales')
ax2 = ax.twinx()
ax2.plot(sales_per_item.index, sales_per_item.values, color='r', label='Price Each')

ax.set_xlabel('Product')
ax.set_ylabel('Total Sales')
ax2.set_ylabel('Price per Product')

# plt.xticks(rotation=90)
plt.ticklabel_format(style = 'plain', axis = 'y')
plt.tight_layout()
plt.setp(ax.get_xticklabels(), rotation = 30, horizontalalignment='right', fontsize='small')


plt.show()


# In[84]:


sales_per_item = sales_data.groupby('Product')['Price Each'].unique()
sales_per_item = sales_per_item.sort_index()

sales_per_item_sales = sales_data.groupby('Product')['Order ID'].count()
sales_per_item_sales = sales_per_item_sales.sort_index()

fig, ax = plt.subplots(figsize=(12, 8))

ax.bar(sales_per_item_sales.index, sales_per_item_sales.values, color='b', label='Total Sales')
ax2 = ax.twinx()
ax2.plot(sales_per_item.index, sales_per_item.values, color='r', label='Price Each')

ax.set_xlabel('Product')
ax.set_ylabel('Total Orders')
ax2.set_ylabel('Price per Product')

# plt.xticks(rotation=90)
plt.ticklabel_format(style = 'plain', axis = 'y')
plt.tight_layout()
plt.setp(ax.get_xticklabels(), rotation = 30, horizontalalignment='right', fontsize='small')


plt.show()


# The above plots comparing Price per product versus Sales generated from each product and Price per product versus Total orders per Product show that the most expensive products generated most sales despite having less ordered quantities as compared to the cheaper products.
# This means that the company should prioritize on increasing sales of the cheaper products by complementing these products with others that go along/might need to use the cheaper products
# 
# 

# In[ ]:




