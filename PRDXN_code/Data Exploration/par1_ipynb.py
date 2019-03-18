
# coding: utf-8

# In[74]:


import numpy as np
import sqlite3
import pandas as pd


# In[90]:


#1)Data Exploration and Evaluation

#Viewing the data through table plus for the database.sqlite db
#Listing the columns that are irrelevant  or need cleansing and standardization

#Loading data from sqlite table into a pandas dataframe for cleansing

df=pd.read_csv('lending-club-loan-data/loan.csv')


# In[91]:


print(df.shape)
#Returns(Rows,Columns)


# In[92]:


# Drop unneccesary columns
df = df.drop(['url', 'desc', 'policy_code', 'last_pymnt_d', 'next_pymnt_d', 'earliest_cr_line', 'emp_title','pymnt_plan','policy_code'], axis=1)
df = df.drop(['id', 'title', 'total_rec_int', 'total_rec_late_fee', 'total_rec_prncp', 'zip_code'], axis=1)


# In[93]:


print(df.shape)


# In[94]:


#Get unique values for relevant columns to understand the data distribution 
#Columns: emp_length,loan_status,home_ownership,annual_income

df.emp_length.unique()
df.loan_status.unique()
df.home_ownership.unique()


# In[95]:


#Replacing emp_length with integer values instead of string
df['emp_length'] = df['emp_length'].apply({'n/a':0,'< 1 year':1,'1 year':2,'2 years':3,'3 years':4,'4 years':5,'5 years':6,'6 years':7,'7 years':8,'8 years':9,'9 years':10,'10+ years':11}.get)
#Replacing Nulls with 0
df.emp_length=df.emp_length.replace(np.nan,0)
df.emp_length.unique()


# In[96]:


#DOwnloading the data frame as a csv file to create a tableau vizualization

df.to_csv('part1.csv')


# In[97]:


df.shape


# In[102]:


df.isnull().sum()


# In[ ]:


#Drop fields with more than 80% of null values

df = df.drop(['mths_since_last_delinq'
,'mths_since_last_record'
,'mths_since_last_major_derog'
,'annual_inc_joint'             
,'dti_joint'                    
,'verification_status_joint'
,'open_acc_6m'
,'open_il_6m'                   
,'open_il_12m'                  
,'open_il_24m'                  
,'mths_since_rcnt_il'          
,'total_bal_il'                 
,'il_util'                      
,'open_rv_12m'                  
,'open_rv_24m'                  
,'max_bal_bc'                   
,'all_util'                     
,'inq_fi'                       
,'total_cu_tl'                  
,'inq_last_12m'], axis=1)

