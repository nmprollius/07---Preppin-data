import os
import pandas as pd
import numpy as np

# Download sheet
# url = ' https://drive.google.com/file/d/1b9KuMlut8mO2LR-zpMe6Ek0XDS8Wcj6D/view'
# path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
# pd.read_csv(path).to_csv('preppin data week 44.csv')

# import file
df = pd.read_csv('preppin data week 44.csv').drop(columns=['Unnamed: 0'])

# Clean columns
df.columns = [i.strip().replace(' ','_').lower() for i in df.columns]

# Change Types
df.purchase_date = pd.to_datetime(df.purchase_date,format='%d/%m/%Y')
df.order_date = pd.to_datetime(df.order_date,format='%d/%m/%Y')
df.date_of_order = pd.to_datetime(df.date_of_order,format='%a %d %b %Y')

# Combine 3 data columns to one
df['order_date_1'] = np.where(df.order_date.isna(),df.date_of_order,df.order_date)
df['order_date_1'] = np.where(df.order_date_1.isna(),df.purchase_date,df.order_date_1)
df.drop(columns=['order_date','date_of_order','purchase_date'],inplace=True)
df.rename(columns={'order_date_1':'order_date'},inplace=True)

# Change orer numbers to strings
df.order_number = df.order_number.astype('str')
df.order_number_text = df.order_number.apply(lambda x:x.zfill(6))
# initials
df.customer_initial = df.customer.apply(lambda x: ''.join([x.split()[0][0],x.split()[1][0]]))

# Concatenate order number and initials
df['order_key'] = df.customer_initial + df.order_number_text

# Select columns
df = df[['order_key','order_number', 'customer', 'order_date']]
df.rename(columns={'order_key':'order_id'},inplace=True)

# Save file
df.to_csv('Week 44 output.csv',index=False)
os.startfile('Week 44 output.csv')