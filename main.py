from pprint import pprint
import pandas
import numpy
from pandas import Series, DataFrame

# data = pandas.read_csv('inputs/revenueCSV.csv').to_dict(orient="row")
# type(data)

# xlsx = pandas.ExcelFile('inputs/RearrangedInputData.xlsx')
# revenueData0 = pandas.read_excel(xlsx, 'Revenue')

cipher = pandas.read_excel('inputs/RearrangedInputData.xlsx', 'DecipherDate')
cipher = cipher.rename(index=str, columns={'Cipher':'variable'})
print("/n","**cipher**")
print(cipher.head())
print(list(cipher.columns))

revenue00 = pandas.read_excel('inputs/RearrangedInputData.xlsx', 'Revenue')
print("/n","**revenue00A**")
print(revenue00.head())
print(list(revenue00.columns))
# print(revenue00.count())

# revenue00 = revenue00.loc[revenue00['Cust_ID'].notnull()]
# print("**revenue00B**")
# print(revenue00.head())

revenue01 = revenue00[['Cust_ID','Product',42]]
revenue01['current'] = revenue00[42] > 0
print("/n", "**revenue01**",revenue01.count(), revenue01.shape[0])
print(revenue01.head())

revenueFF = revenue00.loc[revenue00['Product'] == 'FraudFinder']
print("/n", "**revenueFF**")
print(revenueFF.head())

revenueF2 = revenue00.loc[revenue00['Product'] == 'FraudFinder 2.0.']
print("/n", "**revenueF2**")
print(revenueF2.head())

revenueOverlap = pandas.merge(revenueFF, revenueF2, on='Cust_ID')
revenueOverlap['both'] = revenue01.Cust_ID == revenue01.Cust_ID
print("/n", "**revenueOverlap**")
print(revenueOverlap.head())

revenue02 = pandas.melt(revenue00, ['Cust_ID', 'Product'])
revenue02 = pandas.merge(revenue02, cipher, on='variable' )
revenue02 = revenue02.sort_values(by=['Cust_ID', 'Product', 'variable'])
revenue02.value = revenue02.value.round(0)
revenue02 = revenue02[revenue02['value'] != 0]
print("/n", "**revenue02**")
print(revenue02)

revenue03 = revenue02['value'].groupby([revenue02['Cust_ID'],revenue02['Product'],revenue02['value'],revenue02['Year']]).count()
# revenue03 = revenue03.sort_values(by=['Cust_ID', 'Product', 'Year'])
print("/n", "**revenue03**")
print(revenue03)

revenue04 = revenue02['variable'].groupby([revenue02['Cust_ID'],revenue02['Product'],revenue02['value'],revenue02['Year']]).min()
# revenue03 = revenue03.sort_values(by=['Cust_ID', 'Product', 'Year'])
print("/n", "**revenue04**")
print(revenue04)

customer5 = revenue03['CUSTOMER 5']
print("/n", "**customer5**")
print(customer5)

usage2010 = pandas.read_excel('inputs/RearrangedInputData.xlsx', 'Usage2010')
usage2010['Year']='2010'
usage2011 = pandas.read_excel('inputs/RearrangedInputData.xlsx', 'Usage2011')
usage2011['Year']='2011'
usage2012 = pandas.read_excel('inputs/RearrangedInputData.xlsx', 'Usage2012')
usage2012['Year']='2012'
usage = pandas.concat([usage2010,usage2011,usage2012])
# usage = usage.drop('Unnamed: 0')
print("/n", "**usage**")
print(usage)

growEval1 = pandas.merge(usage2010,usage2011, on='Customer')
print(list(growEval1.columns))
growEval2 = pandas.merge(usage2011,usage2012, on='Customer')
print(list(growEval1.columns))
growEval = pandas.concat([growEval1,growEval2])
growEval['eval'] = growEval['# Transactions_y']>growEval['# Transactions_x']
print("/n", "**growEval**")
print(growEval)

growEvalTrue = growEval[growEval['eval']==True]
growEvalTrue = growEvalTrue[growEvalTrue['# Transactions_x']>0]
print("/n", "**growEvalTrue**")
print(growEvalTrue.iloc[9])

growEvalTrue['change'] = growEvalTrue.apply(lambda row: (row['# Transactions_y']+1) / (row['# Transactions_x']+1), axis=1)
print("/n", "**growEvalTrue**")
print(growEvalTrue)

