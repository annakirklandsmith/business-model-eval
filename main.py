from pprint import pprint
import pandas
import numpy
from pandas import Series, DataFrame

print("\n", "*********************************************", "\n")

cipher = pandas.read_excel('inputs/RearrangedInputData.xlsx', 'DecipherDate')
cipher = cipher.rename(index=str, columns={'Cipher':'variable'})
# print("\n","**cipher**")
# print(cipher.head())
# print(list(cipher.columns))

revenue00 = pandas.read_excel('inputs/RearrangedInputData.xlsx', 'Revenue')
print("\n","**revenue00A**")
print(revenue00.head())
print(list(revenue00.columns))
# print(revenue00.count())

revenueFF = revenue00.loc[revenue00['Product'] == 'FraudFinder']
# print("\n", "**revenueFF**")
# print(revenueFF.head())

revenueF2 = revenue00.loc[revenue00['Product'] == 'FraudFinder 2.0.']
# print("\n", "**revenueF2**")
# print(revenueF2.head())

revenueOverlap = pandas.merge(revenueFF, revenueF2, on='Cust_ID')
revenueOverlap = revenueOverlap[['Cust_ID']]
revenueOverlap['both'] = 'both'
print("\n", "**revenueOverlap**")
print(revenueOverlap.head())

revenue02 = pandas.melt(revenue00, ['Cust_ID', 'Product'])
revenue02 = pandas.merge(revenue02, cipher, on='variable' )
revenue02 = revenue02.sort_values(by=['Cust_ID', 'Product', 'variable'])
revenue02.value = revenue02.value.round(0)
revenue02 = revenue02[revenue02['value'] != 0]
print("\n", "**revenue02**")
print(revenue02.head())

valueGroup = revenue02['value'].groupby([revenue02['Cust_ID'],revenue02['Product'],revenue02['value'],revenue02['Year']])

valueCount = valueGroup.count().reset_index(name="valueCount")
# print("\n", "**valueCount**")
# print(valueCount)
# print(list(valueCount.columns))

variableGroup = revenue02['variable'].groupby([revenue02['Cust_ID'],revenue02['Product'],revenue02['value'],revenue02['Year']])

variableMin = variableGroup.min().reset_index(name="variableMin")
# print("\n", "**variableMin**")
# print(variableMin)
# print(list(variableMin.columns))

variableMax = variableGroup.max().reset_index(name="variableMax")
# print("\n", "**variableMax**")
# print(variableMax)
# print(list(variableMax.columns))

variableMinMax = pandas.merge(variableMin, variableMax, on=('Cust_ID', 'Product', 'value', 'Year'))

revenue06 = pandas.merge(valueCount, variableMinMax, on=('Cust_ID', 'Product', 'value', 'Year'))
# print("\n", "**revenue06**")
# print(revenue06)

variableBigGroup = revenue02['variable'].groupby([revenue02['Cust_ID'],revenue02['Product']])

variableFirst = variableBigGroup.min().reset_index(name="variableFirst")
# print("\n", "variableFirst**")
# print(variableFirst)

variableLast = variableBigGroup.max().reset_index(name="variableLast")
# print("\n", "variableLast**")
# print(variableLast)

assessFirst = variableFirst['variableFirst'].groupby([variableFirst['variableFirst']]).count().reset_index(name="assessFirst")
assessLast = variableLast['variableLast'].groupby([variableLast['variableLast']]).count().reset_index(name="assessLast")
assess = pandas.merge(assessFirst, assessLast, left_on='variableFirst', right_on='variableLast')
assess['delta'] = assess['assessFirst'] - assess['assessLast']
assess = assess[assess['variableFirst'] != 1]
assess = assess[assess['variableLast'] != 42]
assess['favorable'] = assess['delta']>0
print("\n", "**assess**")
print(assess)
assessment = assess['favorable'].groupby([assess['favorable']]).count()
print("\n", "**assessment**")
print(assessment)


revenue07 = pandas.merge(variableFirst, variableLast, on=('Cust_ID', 'Product'))
# print("\n", "**revenue07**")
# print(revenue07)

revenue08 = pandas.merge(revenue06, revenue07, on=('Cust_ID', 'Product'))
# print("\n", "**revenue08**")
# print(revenue08)

variableYearGroup = revenue02['variable'].groupby([revenue02['Cust_ID'],revenue02['Product'],revenue02['Year']])

variableYearCount = variableYearGroup.count().reset_index(name="variableYearCount")
# print("\n", "variableYearCount**")
# print(variableYearCount)

revenue09 = pandas.merge(revenue08, variableYearCount, on=('Cust_ID', 'Product', 'Year'))
# print("\n", "**revenue09**")
# print(revenue09)

revenue10 = pandas.merge(revenue09, revenueOverlap, on=('Cust_ID'), how='left')
revenue10 = revenue10.rename(index=str, columns={'Cust_ID':'Customer'})
# revenue10['Year'].dtype.kind
# treat_str(revenue10['Year'])
# revenue10['Year'] = revenue10['Year'].astype('object')
revenue10['current'] = revenue10['variableLast']==42
# print("\n", "**revenue10**")
# print(revenue10)
# print(revenue10['Year'].dtype)

# customer5 = revenue03['CUSTOMER 5']
# print("/n", "**customer5**")
# print(customer5)

usage2010 = pandas.read_excel('inputs/RearrangedInputData.xlsx', 'Usage2010')
usage2010['Year']=2010
usage2011 = pandas.read_excel('inputs/RearrangedInputData.xlsx', 'Usage2011')
usage2011['Year']=2011
usage2012 = pandas.read_excel('inputs/RearrangedInputData.xlsx', 'Usage2012')
usage2012['Year']=2012
usage = pandas.concat([usage2010,usage2011,usage2012])

# print("\n", "**usage**")
# print(usage)
# print(usage['Year'].dtype)

revenue11 = pandas.merge(revenue10,usage, on=('Customer', 'Year'), how='left')
revenue11['interval'] = revenue11['variableLast']-revenue11['variableFirst']+1
revenue11['transProp'] = revenue11['valueCount'] / revenue11['variableYearCount']
revenue11['transPerMonth'] = revenue11['transProp']*revenue11['# Transactions']
revenue11['bill'] = revenue11['value']*revenue11['valueCount']
revenue11['rate'] = revenue11['bill']/revenue11['transPerMonth']
print("\n", "**revenue11**")
print(revenue11)

revenue11.to_excel('inputs/Output1.xlsx', 'Output1')



# customer3 = revenue11['CUSTOMER 3']
# print("\n", "**customer3**")
# print(customer3)

# growEval1 = pandas.merge(usage2010,usage2011, on='Customer')
# print(list(growEval1.columns))
# growEval2 = pandas.merge(usage2011,usage2012, on='Customer')
# print(list(growEval1.columns))
# growEval = pandas.concat([growEval1,growEval2])
# growEval['eval'] = growEval['# Transactions_y']>growEval['# Transactions_x']
# print("/n", "**growEval**")
# print(growEval)

# # Where did this come from? Copy paste error?
# # revenue03 = revenue02['value'].groupby([revenue02['Cust_ID'],revenue02['Product'],revenue02['value'],revenue02['Year']]).count()
# # # revenue03 = revenue03.sort_values(by=['Cust_ID', 'Product', 'Year'])
# # print("/n", "**revenue03**")
# # print(revenue03)
# # print(list(revenue03.columns))

# growEvalTrue = growEval[growEval['# Transactions_x']>0]
# print("/n", "**growEvalTrue**")
# print(growEvalTrue.iloc[9])

# growEvalTrue['change'] = growEvalTrue.apply(lambda row: (row['# Transactions_y']+1) / (row['# Transactions_x']+1), axis=1)
# print("/n", "**growEvalTrue**")
# print(growEvalTrue)

# growEvalNarrow = growEvalTrue[growEvalTrue['change']<2]
# print("/n", "**growEvalNarrow**")
# print(growEvalNarrow)
# print(growEvalNarrow.describe())