# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 15:38:20 2024

@author: akinola
"""
import webbrowser
import pandas as pd
import numpy as np
import seaborn as sns
from sqlalchemy import create_engine
import pyodbc
sns.set_style("darkgrid")

#section to create connection to local database
connection = 'mssql+pyodbc://localhost/personal_database?trusted_connection=yes&driver=ODBC+driver+17+for+Sql+server'
storage = create_engine(connection)




'''_________________________________________________time-based analysis________________________________________________'''
# reading in required data
transactions = pd.read_csv(
    "C:/Users/akinola/Documents/python DATA ANALYTICS files/Pandas Course Resources/project_data/project_transactions.csv",
    usecols=['household_key','BASKET_ID','DAY','PRODUCT_ID','QUANTITY','SALES_VALUE'],
    dtype={'DAY':'int16','QUANTITY':'int8','PRODUCT_ID':'int32'},
    )
transactions['PRODUCT_ID']=transactions['PRODUCT_ID'].abs()

#-------------------------------------------------------------------------|
transactions =(transactions
               .assign(
                   date= ( pd.to_datetime('2016',format = '%Y')
               +
               pd.to_timedelta(transactions['DAY'].sub(1),unit='D')
               ) )
               .set_index("date")
               .sort_index()
               )
#-------------------------------------------------------------------------\
    
#- plot the sum of sales by month, are sales growing over time?
# print(transactions.resample("M").sum().SALES_VALUE.plot(title='sum of sales over time',ylabel='sales value'))

#next, plot the same series after filtering down to the dates April 2016 and October 2017
# print(transactions.loc['2016-04':'2017-10'].resample("M").sum().plot(y= 'SALES_VALUE',title = 'sum of sales from april 2017 to october 2017',ylabel='sales value'))

# then, plot the sum of monthly sales in 2016 vs the monthly sales 2017
transactions['month']=pd.to_datetime(transactions.index).to_series().dt.strftime("%B")
transactions['year'] = pd.to_datetime(transactions.index).year
transactions = transactions.sort_index()
pivoted = transactions.pivot_table(
    index = 'month',
    columns = 'year',
    values = 'SALES_VALUE',
    aggfunc = 'sum'
    )
pivoted_heat = pivoted.style.background_gradient(cmap="RdYlGn",axis=1)
pivoted_html = "2016vs2017 sales value data.html"
pivoted_heat.to_html(pivoted_html)
# print(pivoted.plot(),pivoted.plot.bar(title="2016 vs 2017 sales data",ylabel='sales value'))
# webbrowser.open(pivoted_html)

#finally, plot total sales by the day of the week
transactions['weekday'] = pd.to_datetime(transactions.index).to_series().dt.strftime("%A")
# print(transactions.groupby('weekday')[['SALES_VALUE']].sum().sort_values(by='SALES_VALUE',ascending=True).plot.barh(title='sum of sales by day of week',colormap='Set2',ylabel='sales value'))

'''________________________________________________________________________________________________________________'''



'''_____________________________________________Demograph analysis________________________________________________'''
#reading in required file
demograph = pd.read_csv(
    "C:/Users/akinola/Documents/python DATA ANALYTICS files/Pandas Course Resources/project_data/hh_demographic.csv",
    usecols = ['AGE_DESC','INCOME_DESC','HH_COMP_DESC','household_key','HOMEOWNER_DESC'],
    dtype={"household_key":"int16"}
    )

#group the transactions table by ``household_id`` and calculate the sum of ``sales_value`` by household
sales_by_household = transactions.groupby("household_key")[['SALES_VALUE']].sum()

#join the demographics dataframe to the aggregated transactions table
sales_by_demograph = pd.merge(sales_by_household,demograph,on='household_key',how='inner')
# print(sales_by_demograph.head())

#plot the sum of sales by ``age_desc`` and ``income_desc``(in separate charts)
#age_desc
# print(sales_by_demograph.groupby("AGE_DESC")[['SALES_VALUE']].sum().plot.bar(title='sum of houshold sales by age demography',ylabel='sales value'))
#income desc
# print(sales_by_demograph.groupby("INCOME_DESC")[['SALES_VALUE']].sum().plot.bar(title = 'sum of household sales by income demography',ylabel='sales value'))


#______________________________________________

#-------------------------------------------------------------------------------------\
#HOMEOWNER_DESC
# Droping missing values in relevant columns
sales_by_demograph = sales_by_demograph.dropna(subset=['AGE_DESC', 'INCOME_DESC', 'HOMEOWNER_DESC'])

#defining conditions and choices for age, income, and homeowner status
#AGE
condition = [
    (sales_by_demograph['AGE_DESC'] == '65+'),
    (sales_by_demograph['AGE_DESC'] == '55-64'),
    (sales_by_demograph['AGE_DESC'] == '45-54'),
    (sales_by_demograph['AGE_DESC'] == '35-44'),
    (sales_by_demograph['AGE_DESC'] == '25-34'),
    (sales_by_demograph['AGE_DESC'] == '19-24')
]
choice = [80, 64, 54, 44, 34, 24]

#INCOME
condlist = [
    (sales_by_demograph['INCOME_DESC'] == '250K+'),
    (sales_by_demograph['INCOME_DESC'] == '200-249K'),
    (sales_by_demograph['INCOME_DESC'] == '175-199K'),
    (sales_by_demograph['INCOME_DESC'] == '150-174K'),
    (sales_by_demograph['INCOME_DESC'] == '125-149K'),
    (sales_by_demograph['INCOME_DESC'] == '100-124K'),
    (sales_by_demograph['INCOME_DESC'] == '75-99K'),
    (sales_by_demograph['INCOME_DESC'] == '50-74K'),
    (sales_by_demograph['INCOME_DESC'] == '35-49K'),
    (sales_by_demograph['INCOME_DESC'] == '25-34K'),
    (sales_by_demograph['INCOME_DESC'] == '15-24K'),
    (sales_by_demograph['INCOME_DESC'] == 'Under 15K')
]
choicelist = [300, 249, 199, 174, 149, 124, 99, 74, 49, 34, 24, 15]

#HOMEOWNER STATUS
cond = [
    (sales_by_demograph['HOMEOWNER_DESC'] == 'Homeowner'),
    (sales_by_demograph['HOMEOWNER_DESC'] == 'Unknown'),
    (sales_by_demograph['HOMEOWNER_DESC'] == 'Renter'),
    (sales_by_demograph['HOMEOWNER_DESC'] == 'Probable Renter'),
    (sales_by_demograph['HOMEOWNER_DESC'] == 'Probable Owner')
]
choice_list = [1, 2, 3, 4, 5]

# Creating new columns based on conditions
sales_by_demograph['owner_dist'] = np.select(cond, choice_list, default='unavailable')
sales_by_demograph['age_dist'] = np.select(condition, choice, default='unavailable')
sales_by_demograph['income_dist'] = np.select(condlist, choicelist, default='unavailable')

# Converting new columns to numeric, coercing errors to NaN
sales_by_demograph['age_dist'] = pd.to_numeric(sales_by_demograph['age_dist'], errors='coerce')
sales_by_demograph['income_dist'] = pd.to_numeric(sales_by_demograph['income_dist'], errors='coerce')
sales_by_demograph['owner_dist'] = pd.to_numeric(sales_by_demograph['owner_dist'], errors='coerce')

# Droping rows with NaN values in new columns
sales_by_demograph = sales_by_demograph.dropna(subset=['age_dist', 'income_dist', 'owner_dist'])

# Creating scatter plot
# print(sales_by_demograph.plot.scatter(x='HOMEOWNER_DESC',
#                                      y='income_dist',
#                                      c= 'age_dist', # Use 'owner_dist' column for color
#                                      cmap='Set2',
#                                       # figsize=(10, 10)
#                                      ))

#--------------------------------------------------------------------------------------\

#pivot table of the mean households sales by ``age_desc`` and ``ee_comp_desc``
household_mean_by_age =( sales_by_demograph
                        .pivot_table(
                            index='AGE_DESC',
                            columns = 'HH_COMP_DESC',
                            values = 'SALES_VALUE',
                            aggfunc='mean'))

#Which of our demographics have the highest average sales? 

#           to generate heatmap 
# house_heat = household_mean_by_age.style.background_gradient(cmap="RdYlGn",axis=0)
# demo_heat = "demograph heat.html"
# house_heat.to_html(demo_heat)
# webbrowser.open(demo_heat)
# print(household_mean_by_age.max())
'''____________________________________________________________________________________________________________'''



'''________________________________________________product demograph___________________________________________'''

#reading in required data
product = pd.read_csv(
    "C:/Users/akinola/Documents/python DATA ANALYTICS files/Pandas Course Resources/project_data/product.csv",
    
    usecols=['PRODUCT_ID','DEPARTMENT'],dtype={"PRODUCT_ID":"int32"}
    )
# #Join the product dataframe  to transactions and demographics tables

proTran = pd.merge(transactions.merge(product,on='PRODUCT_ID',how='inner'),
                   demograph,on='household_key',how='inner')
proTran['DEPARTMENT'],proTran['SALES_VALUE'] = (proTran['DEPARTMENT'].replace({" ":"unknown"}),
                                                proTran['SALES_VALUE'].fillna(0))

# pivot the fully joined dataframe by ``age_desc`` and ``department``,calculating the sum 
demo_performance =( proTran
                   .pivot_table(
                       index ='DEPARTMENT',
                       columns = 'AGE_DESC',
                       values = 'SALES_VALUE',
                       aggfunc = 'sum'
                       ))
demo_performance = demo_performance.fillna(0)
Agedemo_heat = demo_performance.style.background_gradient(cmap="RdYlGn",axis=1)
demo_html = 'perfomance by age demograph.html'
Agedemo_heat.to_html(demo_html)
# webbrowser.open(demo_html)



'''______________________________________________storage section_______________________________________________'''
#section to store summary table in local database and flat files
# conn = pyodbc.connect(
#     'DRIVER = {ODBC DRIVER 17 FOR SQL SERVER};\
#     SERVER= localhost;\
#     DATABASE= master ;\
#     trusted_connection = yes'
#     )

# cursor = conn.cursor()

# cursor.execute("CREATE DATABASE final_project")

# conn.commit()
# cursor.close()
# conn.close()

#storing merged data into local database
proTran_sqltable = proTran.to_sql(
    name='summary table of product demograph',
    con=storage,
    if_exists = 'append'
    )

#exporting to excel format
demo_performance_xlsx = Agedemo_heat.to_excel("product transactions demograph.xlsx",sheet_name='sales_pivot')
#exporting to csv
demo_performance_csv = demo_performance.to_csv("product transactions demograpg.csv")

