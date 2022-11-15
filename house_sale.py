def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,PolynomialFeatures
from sklearn.linear_model import LinearRegression
# %matplotlib inline

file_name='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/FinalModule_Coursera/data/kc_house_data_NaN.csv'
df=pd.read_csv(file_name)
# print(df.head())
print(df.dtypes)
df.drop(["id","Unnamed: 0"],axis=1,inplace=True)
print(df.describe())
# print("number of NaN values for the column bedrooms :", df['bedrooms'].isnull().sum())
# print("number of NaN values for the column bathrooms :", df['bathrooms'].isnull().sum())
mean = df["bedrooms"].mean()
df["bedrooms"].replace(np.nan,mean,inplace=True)
mean = df["bathrooms"].mean()
df["bathrooms"].replace(np.nan,mean,inplace=True)
# print("number of NaN values for the column bedrooms :", df['bedrooms'].isnull().sum())
# print("number of NaN values for the column bathrooms :", df['bathrooms'].isnull().sum())
# Module 3: Exploratory Data Analysis
floor_counts = df["floors"].value_counts().to_frame()
print(floor_counts)
# Question 4
sns.boxplot(x="waterfront",y="price",data=df)
plt.show()
# Question 5
sns.regplot(x="sqft_above",y="price",data=df)
plt.show()
# print(df.corr()['price'].sort_values())
X= df[['long']]
Y= df['price']
lm = LinearRegression()
lm.fit(X,Y)
print(lm.score(X,Y))
# Question  6
X1 = df[['sqft_living']]
Y1 = df['price']
lm1 = LinearRegression()
lm1.fit(X1,Y1)
print('the R-square:', lm1.score(X1,Y1))
# Question 7
features =["floors", "waterfront","lat" ,"bedrooms" ,"sqft_basement" ,"view" ,"bathrooms","sqft_living15","sqft_above","grade","sqft_living"]     
Z = df[features]
Z = Z.astype(float)
Y = df['price']
lm2 = LinearRegression()
lm2.fit(Z,Y)
print('the R-square:', lm2.score(Z,Y))
# Question 8
Input=[('scale',StandardScaler()),('polynomial', PolynomialFeatures(include_bias=False)),('model',LinearRegression())]
features =["floors", "waterfront","lat" ,"bedrooms" ,"sqft_basement" ,"view" ,"bathrooms","sqft_living15","sqft_above","grade","sqft_living"]     
Z = df[features]
Z = Z.astype(float)
Y = df['price']
pipe = Pipeline(Input)
pipe.fit(Z,Y)
print('the R-square:',pipe.score(Z,Y))

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
features =["floors", "waterfront","lat" ,"bedrooms" ,"sqft_basement" ,"view" ,"bathrooms","sqft_living15","sqft_above","grade","sqft_living"]
X= df[features]
Y= df['price']
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.15, random_state=1)
# print("number of test samples:", x_test.shape[0])
# print("number of training samples:",x_train.shape[0])
# Question 9
RidgeModle = Ridge(alpha=0.1)
RidgeModle.fit(x_train,y_train)
print('the R-square:',RidgeModle.score(x_test,y_test))
# Question 10
features =["floors", "waterfront","lat" ,"bedrooms" ,"sqft_basement" ,"view" ,"bathrooms","sqft_living15","sqft_above","grade","sqft_living"]
pr = PolynomialFeatures(degree=2)
x_test_pr = pr.fit_transform(x_test[features])
x_train_pr = pr.fit_transform(x_train[features])
Rd = Ridge(alpha=0.1)
Rd.fit(x_train_pr,y_train)
print('the R-square:',Rd.score(x_test_pr,y_test))