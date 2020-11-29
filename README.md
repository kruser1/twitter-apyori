# twitter-apyori
A demonstration of association rule learning with Twitter data and Python's apyori package.


# IT_631_Machine Learning_Final project_Fall2020-(README)

[1] Title:
	-A Framework for Association Rule Learning with Social Media Networks.

[2] Team:
	-Ryan Kruse and Tharindu Lokukatagoda,
	-Done under the guidance of Dr.Suboh Alkhushayni.

[3] Description:
	Association rule learning might be used to identify which items are most and least likely to be bought with bread at Walmart. One might discover that when peanut butter is bought, bread is also frequently bought, but when bread is bought, peanut butter might not be as frequently bought (people who buy peanut butter usually buy bread but people who buy bread don’t necessarily want peanut butter with it). In our context, we can think of “following Donald Trump on Twitter” as “buying bread at Walmart,” “following Andrew Yang on Twitter” as “buying peanut butter at Walmart,” and “following Elon Musk on Twitter” as “buying jelly at Walmart.” A “transaction” is a Twitter account’s following list. Just like in market basket analysis when we want to analyze all transactions where bread is purchased, we can analyze all Twitter accounts that follow Donald Trump. Then, asking “What is the relationship between Andrew Yang and Elon Musk on Twitter among Trump’s Twitter followers” is like asking “When bread is purchased, what is the relationship between peanut butter and jelly?” In this study we are trying to apply the relationship between Twitter followers among market basket analysis and analyze user behavior data.

[3] Files:

	- apriori.py
		+ read the data from GitHub and store in pandas dataframes
		+ used matplotlib for visualizing results
	- Twitter API Crawler.ipynb
		+ pull data from the Twitter Apriori
		+ must supply authorization keys

[4] For install and import the program we ran the following commands:
```
import pandas as pd
from apyori import apriori
import matplotlib.pyplot as plt
```

[5] For dataset definition:

	a) Read input files
		- The data set for Biden taken from 'https://raw.githubusercontent.com/kruser1/twitter-apyori/main/twitter_biden.csv'. We deleted all the entries that contains an empty cell in it.
		- The data set for Trump taken from 'https://raw.githubusercontent.com/kruser1/twitter-apyori/main/twitter_trump.csv'. And also, we deleted all the entries that contains an empty cell in it.

[6] example of equation used:

	confidence(X->Y) = support(X U Y) / support(X)
	support(X, Y) = count(X, Y) / total dataset


[7] Data visulaization for association rule:

	- It is always useful to be able create different visualizations.
	- The scatterplot shows us the frequency of plotting symbols and they have a higher of levels of support and the confidence for each of the datasets.
	- The darker shaded plotting symbols mean they have a higher lift.  
	- And here is the python code for scatter plot. Since a few points here have the same values we added small random values to show all points.

	import random
	import matplotlib.pyplot as plt

	#scatter plot
	for i in range (len(support)):
   	support[i] = support[i] + 0.0025 * (random.randint(1,10) - 5)
   	confidence[i] = confidence[i] + 0.0025 * (random.randint(1,10) - 5)

	#Visualizing results: Support vs Confidence
	plt.scatter(support, confidence,c=rules['lift']/max(rules['lift']))#,   alpha=0.5)
	plt.xlabel('support')
	plt.ylabel('confidence')
	plt.show()

.................................................................................................................................................

[8] Full code including comments:

### Install and Import
```
!pip install apyori

import pandas as pd
from apyori import apriori
import matplotlib.pyplot as plt
```
### Apyori: Basic example

This shows a simple example of the apyori package. We include this to show that it is working as expected.

```
transactions = [
    ['beer', 'nuts'],
    ['beer', 'cheese'],
]
results = list(apriori(transactions))
results
```
### Read Data

Read the data from GitHub and store in pandas DataFrames.
```
biden = pd.read_csv('https://raw.githubusercontent.com/kruser1/twitter-apyori/main/twitter_biden.csv', error_bad_lines=False)
biden = biden.rename({'Unnamed: 0': 'account_following'}, axis=1)
biden = biden.set_index('account_following')
biden.head(3)

trump = pd.read_csv('https://raw.githubusercontent.com/kruser1/twitter-apyori/main/twitter_trump.csv')
trump = trump.rename({'Unnamed: 0': 'account_following'}, axis=1)
trump = trump.set_index('account_following')
trump.head(3)
```
### Define Function
This function removes the JoeBiden or realDonaldTrump entry from the DataFrame and puts the data into a format compatible with the apyori.apriori() function.

```
def getAprioriData(df, name='JoeBiden'):
  data = []
  count = 0
  for col in df.columns:
    data.append([])
    for x in df.index:
      if x != name:
        if df.loc[x, col] == 1:
          data[count].append(x)
    count += 1
  return data
```
### Run Apriori

Here we run the apriori algorithm and print the resulting rules for each candidate.

```
data = getAprioriData(biden, 'JoeBiden')
resultsJ = list(apriori(data, min_support=.05))
resultsJ

print(len([x for x in resultsT if len(x[0])>1]))
print(len([x for x in resultsT if len(x[0])==2]))
print(len([x for x in resultsT if len(x[0])==1]))
```
Examine one record more closely.
```
r = [x for x in resultsJ if len(x[0])>1]
print("Entire record:")
print(r[0])
print("\nItemset:")
print(r[0][0])
print("\nSupport for this itemset:")
print(r[0][1])
print("\nEmpty antecedent, both in consequent:")
print(r[0][2][0])
print("\nAntecedent: AOC; Consequent: BarackObama")
print(r[0][2][1])
print("\nAntecedent: BarackObama; Consequent: AOC")
print(r[0][2][2])

data = getAprioriData(trump, 'realDonaldTrump')
resultsT = list(apriori(data, min_support=.05))
resultsT
```
### Define Plotting Functions

These functions will help us to visualize the resulting rules.

```
def getSupports(results):
  unames = []
  supports = []
  for r in results:
    if len(r[0]) == 1:
      unames.append(list(r[0])[0])
      supports.append(r[1])
  df = pd.DataFrame(columns=['account','support'])
  df['account'] = unames
  df['support'] = supports
  df = df.sort_values('support', ascending=False)
  return(df)

def plotSupports(df, title):
  fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
  ax.set_facecolor('#FFFFFF')
  ax.grid(axis='y', linestyle='--')
  ax.set_axisbelow(True)
  plt.bar(df['account'], df['support'], color=df['color'], edgecolor='black', alpha=.7)
  plt.ylabel("support", )
  plt.xticks(rotation=90)
  plt.title(title + "-associated Twitter Accounts")
  plt.ylim((0,.25))

def getColors(uname, df):
  if uname in ['JoeBiden','realDonaldTrump']:
    return('purple')
  if uname in df.account.values:
    x = df.index[df['account'] == uname].tolist()[0]
    return(x)
  return('#BBBBBB')
```
### Plot Support

This plot helps us to compare and contrast the resulting rules.

```
dfj = getSupports(resultsJ)
dft = getSupports(resultsT)

both = [x for x in dfj.account if x in dft.account.values]

dfj['color'] = dfj.apply(lambda row : getColors(row['account'], dft), axis=1)
dft['color'] = dft.apply(lambda row : getColors(row['account'], dfj), axis=1)

colors = ['blue','red','limegreen','yellow','orange','brown']
count = 0
for i, row in dfj[dfj['account'].isin(dft['account'])].iterrows():
  x = row['color']
  dfj.loc[i, 'color'] = colors[count]
  dft.loc[x, 'color'] = colors[count]
  count += 1

plotSupports(dfj, "Biden")
plotSupports(dft, "Trump")
```

### Plot Support, Confidence, and Lift
```
data = getAprioriData(biden, 'realDonaldTrump')
import pandas as pd
from mlxtend.preprocessing import OnehotTransactions
from mlxtend.frequent_patterns import apriori

#cleaning up data (divided to columns)
oht = OnehotTransactions()
oht_ary = oht.fit(data).transform(data)
df = pd.DataFrame(oht_ary, columns=oht.columns_)

resultsTable = apriori(df, min_support=.05, use_colnames=True)
print(resultsTable)

#This function allows us to (1) specify our metric of interest and (2) the according threshold.
 #Implemented measures are confidence and lift.
from mlxtend.frequent_patterns import association_rules

association_rules(resultsTable, metric="confidence", min_threshold=0.7)
#To have a lift score of >=1.2, we ran the following step:
rules = association_rules(resultsTable, metric="lift", min_threshold=1.2)
print (rules)

#declaring support and confidence variables
support=rules['support'].values
confidence=rules['confidence'].values

import random
import matplotlib.pyplot as plt

#scatter plot
for i in range (len(support)):
   support[i] = support[i] + 0.0025 * (random.randint(1,10) - 5)
   confidence[i] = confidence[i] + 0.0025 * (random.randint(1,10) - 5)

#Visualizing results: Support vs Confidence
plt.scatter(support, confidence,c=rules['lift']/max(rules['lift']), s=500,   alpha=0.5)
plt.xlabel('support')
plt.ylabel('confidence')
plt.gray()
plt.title("Trump-associated Rules")
plt.show()
```
