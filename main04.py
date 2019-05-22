#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas
from pandas import Series, DataFrame


# ## cipher table

# Later, it proves to be a hurdle that pandas recognizes the revenue date columns as dates. To simplify matters, I decided to rename the columns by integer series to represent 42 months. In preparation, I make the cipher table:

# In[2]:


precipher = {'variable': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
             'Year': [2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2011, 2011, 2011, 2011, 2011, 2011, 2011, 2011, 2011, 2011, 2011, 2011, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2012, 2013, 2013, 2013, 2013, 2013, 2013]}
cipher = pandas.DataFrame(precipher)
cipher.head()
    


# ## revenue table (crosstab orientation)

# In[3]:


revenue00 = pandas.read_excel('inputs/2014 FraudFinder Case Study - Data Set.xlsx', 'Revenue', skiprows=[0,1,2])
revenue00.head()


# In[4]:


for i in range(3,45):
    revenue00.rename(columns={revenue00.columns[i]: i-2}, inplace=True)
revenue00.drop(['Unnamed: 0'], axis=1)
revenue00 = revenue00.rename(index=str, columns={'Product Group':'Product'})


# ## find which customers use both FraudFinder and FraudFinder 2.0.

# In[5]:


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


# ## transpose revenue table, find out interesting things about subgroups, and join all findings

# In[6]:


revenue02 = pandas.melt(revenue00, ['Cust_ID', 'Product'])
revenue02 = pandas.merge(revenue02, cipher, on='variable' )
revenue02 = revenue02.sort_values(by=['Cust_ID', 'Product', 'variable'])
revenue02 = revenue02[revenue02['value'] != 0]
print("\n", "**revenue02**")
print(revenue02.head())


# In[7]:


variableGroup = revenue02['variable'].groupby([revenue02['Cust_ID'],revenue02['Product'],revenue02['Year']])

variableMin = variableGroup.min().reset_index(name="variableMin")
# print("\n", "**variableMin**")
# print(variableMin)
# print(list(variableMin.columns))

variableMax = variableGroup.max().reset_index(name="variableMax")
# print("\n", "**variableMax**")
# print(variableMax)
# print(list(variableMax.columns))

variableMinMax = pandas.merge(variableMin, variableMax, on=('Cust_ID', 'Product', 'Year'))
# print("\n", "**variableMinMax**")
# print(variableMinMax)
# print(list(variableMinMax.columns))

revenue06 = pandas.merge(revenue02, variableMinMax, on=('Cust_ID', 'Product', 'Year'))
# print("\n", "**revenue06**")
# print(revenue06)

revenue06.head()


# ## Notice how most months see more customer volume losses, not gains

# In[8]:


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
print(assess.head())
assessment = assess['favorable'].groupby([assess['favorable']]).count()
print("\n", "**assessment**")
print(assessment)


# ## Resume expanding transposed revenue table

# In[9]:


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


# In[10]:


revenue10 = pandas.merge(revenue09, revenueOverlap, on=('Cust_ID'), how='left')
revenue10 = revenue10.rename(index=str, columns={'Cust_ID':'Customer'})

revenue10['current'] = (revenue10['variableLast']==42).astype(int)
#print("\n", "**revenue10**")
#print(revenue10)
revenue10.head()


# ## prepare usage table about transaction history

# In[11]:


usagepre = pandas.read_excel('inputs/2014 FraudFinder Case Study - Data Set.xlsx', 'Usage', skiprows=[0,1,2,3])


# In[12]:


usage2010 = usagepre[['Customer','# Transactions']].dropna()
usage2010['Year']=2010
usage2011 = usagepre[['Customer.1','# Transactions.1']].dropna().rename(index=str, columns={'Customer.1':'Customer', '# Transactions.1':'# Transactions'})
usage2011['Year']=2011
usage2012 = usagepre[['Customer.2','# Transactions.2']].dropna().rename(index=str, columns={'Customer.2':'Customer', '# Transactions.2':'# Transactions'})
usage2012['Year']=2012


# In[13]:


usage = pandas.concat([usage2010,usage2011,usage2012])
usage


# ## Review compound interest 
# Goal: get a monthly increment that results in a yearly increment of 10%

# In[14]:


# Python3 program to find compound 
# interest for given values. 

def compound_interest(principle, rate, time): 

	# Calculates compound interest 
	CI = principle * (pow((1 + rate / 100), time)) 
	print("Compound interest is", CI) 

# Driver Code 
compound_interest(1, 10/12, 1) 

# This code is contributed by Abhishek Agrawal at https://www.geeksforgeeks.org/python-program-for-compound-interest/


# ## Expand transposed revenue table with usage data and new fields 
# To prepare for correlation between simulated business model 'compound' and cost per transaction 'rate'

# In[15]:


revenue11 = pandas.merge(revenue10,usage, on=('Customer', 'Year'), how='inner')
revenue11['interval'] = revenue11['variableLast']-revenue11['variableFirst']+1
revenue11['transProp'] = 1 / revenue11['variableYearCount']
revenue11['transPerMonth'] = revenue11['transProp']*revenue11['# Transactions']
revenue11['item'] = revenue11['variable']-revenue11['variableMin']+1
revenue11['compound'] = (1 * (pow((1 + (10/12)/100), revenue11['item']))).astype(float)    
revenue11['rate'] = revenue11['value']/revenue11['transPerMonth']
revenue11.head()


# ## Get a subset of data we can trust
# Calculations don't happen on zeros.
# Also, some products use both products; using their data creates confusion
# Also, the business model is for the last three years

# In[16]:



revenue12 = revenue11[revenue11['both'] != 'both'] 
revenue12 = revenue12[revenue12['# Transactions'] > 0]
revenue12 = revenue12[revenue12['rate'] > 0]
revenue12 = revenue12[revenue12['variable'] > 6]
revenue12 = revenue12[['Customer','Product', 'current','compound','rate']]
revenue12.head()


# ## Find correlation values for each subgroup

# In[17]:


revenue13 = revenue12.groupby([revenue12['Customer'],revenue12['Product'],revenue12['current']]).apply(lambda g: g['compound'].corr(g['rate'])).reset_index(name="corr")
revenue13
print(revenue13['Customer'].dtype)
print(revenue13['Product'].dtype)
print(revenue13['current'].dtype)
print(revenue13['corr'].dtype)


# ## Describe the distribution for each subgroup

# In[18]:


ffCurrent = revenue13[(revenue13['current']==1) & (revenue13['Product']=='FraudFinder')]
print("\n", "**ffCurrent**")
print(ffCurrent.head())
print(ffCurrent.describe())

ffFormer = revenue13[(revenue13['current']==0) & (revenue13['Product']=='FraudFinder')]
print("\n", "**ffFormer**")
print(ffFormer.head())
print(ffFormer.describe())

f2Current = revenue13[(revenue13['current']==1) & (revenue13['Product']=='FraudFinder 2.0.')]
print("\n", "**f2Current**")
print(f2Current.head())
print(f2Current.describe())

f2Former = revenue13[(revenue13['current']==0) & (revenue13['Product']=='FraudFinder 2.0.')]
print("\n", "**ffFormer**")
print(ffFormer.head())
print(ffFormer.describe())

