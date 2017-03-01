import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

## Change the path to where the data is on your computer
## Data found at: https://github.com/ChicagoBoothML/MLClassData/tree/master/CaliforniaHousing
yourPath = 'C:\Users\jbellmas\Documents\Kauffman drive\Code\\'
filename = "ca_housing.csv"
df = pd.read_csv(yourPath+filename)

## Just check out the data a bit
df.info()
df.head()
df.describe()

## Basic pair plots
sns.pairplot(df[["medianIncome", "AveBedrms", "logMedVal"]])
plt.show()

## Let's split into train and test
train = df.sample(frac=0.8, random_state=1)
test = df.loc[~df.index.isin(train.index)]
train.info()
test.info()
## Linear regression, predict logMedVal with medianIncome
## Fit model on training data
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
x = train[["medianIncome"]]
y = train["logMedVal"]
lr.fit(x, y)

## Predict on test data
predictX = test[["medianIncome"]]
predictY = test["logMedVal"]
predictions = lr.predict(predictX)
predictions
len(predictions)

lr.predict(3)
lr.score(x, y)

## Plot our yhats against our y
plt.scatter(predictY, predictions)
plt.show()

## We can do the same with multiple x variables...
x = train[["medianIncome", "AveRooms", "housingMedianAge"]]
lr.fit(x, y)
lr.score(x,y)
predictX = test[["medianIncome", "AveRooms", "housingMedianAge"]]
predictions = lr.predict(predictX)
plt.show()

## What about more advanced models?  Easy with sklearn...
from sklearn.ensemble import RandomForestRegressor
x = train[["medianIncome", "AveRooms", "housingMedianAge"]]
rf = RandomForestRegressor(n_estimators=100, min_samples_leaf=3)
rf.fit(x, y)
predictions = rf.predict(predictX)
from sklearn.metrics import mean_squared_error
mean_squared_error(predictY, predictions)
