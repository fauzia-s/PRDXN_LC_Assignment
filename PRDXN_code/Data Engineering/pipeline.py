
import numpy as np
import sqlite3
import pandas as pd
import os
import datetime



#Load the loan.csv into a dataframe
df=pd.read_csv('lending-club-loan-data/loan.csv')




#Check the quality of file if corrupted,send an email to the SME and exit the process

#Assign the fields to a header to match with the file
header=['index','id'
 'member_id',
 'loan_amnt',
 'funded_amnt',
 'funded_amnt_inv',
 'term',
 'int_rate',
 'installment',
 'grade',
 'sub_grade',
 'emp_length',
 'home_ownership',
 'annual_inc',
 'verification_status',
 'issue_d',
 'loan_status',
 'purpose',
 'addr_state',
 'dti',
 'delinq_2yrs',
 'inq_last_6mths',
 'mths_since_last_delinq',
 'mths_since_last_record',
 'open_acc',
 'pub_rec',
 'revol_bal',
 'revol_util',
 'total_acc',
 'initial_list_status',
 'out_prncp',
 'out_prncp_inv',
 'total_pymnt',
 'total_pymnt_inv',
 'recoveries',
 'collection_recovery_fee',
 'last_pymnt_amnt',
 'last_credit_pull_d',
 'collections_12_mths_ex_med',
 'mths_since_last_major_derog',
 'application_type',
 'annual_inc_joint',
 'dti_joint',
 'verification_status_joint',
 'acc_now_delinq',
 'tot_coll_amt',
 'tot_cur_bal',
 'open_acc_6m',
 'open_il_6m',
 'open_il_12m',
 'open_il_24m',
 'mths_since_rcnt_il',
 'total_bal_il',
 'il_util',
 'open_rv_12m',
 'open_rv_24m',
 'max_bal_bc',
 'all_util',
 'total_rev_hi_lim',
 'inq_fi',
 'total_cu_tl',
 'inq_last_12m']

# if df.shape[0] == 0 or df.shape[1]==0:
# 	exit()
# else if list(df.columns) <> l:
#     exit()



#File looks good,so let's proceed with cleansing

#Dropping unecessary fields (may vary based on downstream reqs)
df = df.drop(['url', 'desc', 'policy_code', 'last_pymnt_d', 'next_pymnt_d', 'earliest_cr_line','pymnt_plan','policy_code'], axis=1)
df = df.drop(['total_rec_int', 'total_rec_late_fee', 'total_rec_prncp', 'zip_code'], axis=1)

#Standardizing data and replacing Nulls with valid values

#emp_length
df['emp_length'] = df['emp_length'].apply({'n/a':0,'< 1 year':1,'1 year':2,'2 years':3,'3 years':4,'4 years':5,'5 years':6,'6 years':7,'7 years':8,'8 years':9,'9 years':10,'10+ years':11}.get)
#Replacing Nulls with 0
df.emp_length=df.emp_length.replace(np.nan,0)
#df.emp_length.unique()

#application_type
df['application_type']=df['application_type'].apply({'INDIVIDUAL':1,'JOINT':2}.get)
#pd.value_counts(data.application_type).to_frame()
df.application_type=df.application_type.replace(np.nan,0)
#df.application_type.unique()

#term
df['term']=df['term'].apply({' 36 months':36,' 60 months':60}.get)
#df.term.unique()


#Get null counts for remaining fields in the dataframe and remove the fields that have more than 80% nulls
df.isnull().sum()

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


#Data validation: Datatype and range for the relevant fields
#If there's any transformation/derivation of new fields then data validation for them would be included to compare source fields and the derived fields as per transformations
#Loans per id
#Total id counts per country/loan type
#Amount of loan approved/disbursed

##Datatype and range checks for the shortlisted fields
#Using package 'pandas-validation' for validating numerics,strings and datetimes

#Id:long int only, no string,decimals
pv.validate_numeric(
    df.id,
    nullable=False,
    unique=True,
    integer=True,
    return_type=None)


#Term: (Assuming) not less than 6 months and not more than 72 months

pv.validate_numeric(
    df.term,
    nullable=True,
    unique=False,
    integer=True,
    min_value=6,
    max_value=72,
    return_type=None)


#Connect to the sqllite database
cnx = sqlite3.connect("database.sqlite")

#Append the data into the existing sqlite table
#Can include PK constraint to update existing data
df.to_sql('loan_data', cnx, if_exists='append')



#Append the original file with process date and move to archived folder after ETL
now=datetime.datetime.now()
filename="loan-"+now.strftime("%Y-%m-%d-%H-%M-%S-%f")+".csv"
os.replace('pending/loan.csv','processed/'+filename)

#create a CSV file with the clean data just in case
df.to_csv('processed/loan_cleaned_'+filename)





