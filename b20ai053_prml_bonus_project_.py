# -*- coding: utf-8 -*-
"""B20AI053 PRML Bonus Project .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1USgv8isEp4ZhGE1bjJ-6hZe8Sh2Ldttv

##Importing the necessary libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""###Mounting the drive"""

from google.colab import drive
drive.mount('/content/drive')

"""###Loading the dataset"""

df=pd.read_excel('/content/drive/MyDrive/Bonus Project/Dataset.xlsx')
df.head()

"""##Preprocessing"""

df.info()

df.shape

"""###Dropping the rows with null values in some features"""

df.dropna(inplace=True)

df.shape

df.describe()

"""###Viewing the number of unique values in the dataset"""

df.nunique()

for col in df.columns:
  print(df[col].value_counts())
  print('\n')

"""###viewing and dropping the duplicate values"""

df.duplicated().sum()

df.drop_duplicates(keep='first',inplace=True)

df.shape

"""###Preprocessing"""

def change_into_datetime(df,col):
  df[col]=pd.to_datetime(df[col])

dt_cols=['Date_of_Journey','Dep_Time','Arrival_Time']
for i in dt_cols:
  change_into_datetime(df,i)

df.info()

df['Day']=df['Date_of_Journey'].dt.day
df['Month']=df['Date_of_Journey'].dt.month
df.drop('Date_of_Journey',axis=1,inplace=True)

df['Day'].head()

df.info()

def extract_hm(data,col):
    data[col+'_hour']=data[col].dt.hour
    data[col+'_min']=data[col].dt.minute
    data.drop(col,axis=1,inplace=True)

#extracting hours and minutes and then dropping the Dep_time column
extract_hm(df,'Dep_Time')

#extracting hours and minutes and then dropping the Arrival_time column
extract_hm(df,'Arrival_Time')

duration=list(df['Duration'])
for i in range(len(duration)):
    if len(duration[i].split(' '))==2:
        pass
    elif 'h' in duration[i]:
        duration[i]=duration[i] + ' 0m'
    else:
        duration[i]='0h '+ duration[i]

df['Duration']=duration

df.head()

h=lambda x: x.split(' ')[0][0:-1]
m=lambda x: x.split(' ')[1][0:-1]

df['dur_hour']=df['Duration'].apply(h)
df['dur_min']=df['Duration'].apply(m)

df['dur_hour'].head(),df['dur_min'].head()

df.drop('Duration',axis=1,inplace=True)
df.head()

df.info()

df['dur_hour'] = df['dur_hour'].astype(int)
df['dur_min'] = df['dur_min'].astype(int)

categorical_column=[column for column in df.columns if df[column].dtype=='object']
categorical_column

continuous_col =[column for column in df.columns if df[column].dtype!='object']
continuous_col

categorical = df[categorical_column]

categorical.head()

categorical['Airline'].value_counts()

Airline=pd.get_dummies(categorical['Airline'],drop_first=True)

categorical['Source'].value_counts()

source=pd.get_dummies(categorical['Source'],drop_first=True)

categorical['Destination'].value_counts()

destination=pd.get_dummies(categorical['Destination'],drop_first=True)

categorical['Route'].value_counts()

categorical['Route1']=categorical['Route'].str.split('???').str[0]
categorical['Route2']=categorical['Route'].str.split('???').str[1]
categorical['Route3']=categorical['Route'].str.split('???').str[2]
categorical['Route4']=categorical['Route'].str.split('???').str[3]
categorical['Route5']=categorical['Route'].str.split('???').str[4]

categorical.head()

categorical.drop('Route',axis=1,inplace=True)

categorical.isnull().sum()

for i in ['Route3', 'Route4', 'Route5']:
    categorical[i].fillna('None',inplace=True)

categorical.isnull().sum()

for i in categorical.columns:
    print('{} has total {} categories'.format(i,len(categorical[i].value_counts())))

from sklearn.preprocessing import LabelEncoder
le= LabelEncoder()

for i in ['Route1', 'Route2', 'Route3', 'Route4', 'Route5']:
    categorical[i]=le.fit_transform(categorical[i])

categorical.drop('Additional_Info',axis=1,inplace=True)

categorical['Total_Stops'].unique()

dict={'non-stop':0, '2 stops':2, '1 stop':1, '3 stops':3, '4 stops':4}
categorical['Total_Stops']=categorical['Total_Stops'].map(dict)

categorical['Total_Stops']

categorical.drop('Source',axis=1,inplace=True)
categorical.drop('Destination',axis=1,inplace=True)
categorical.drop('Airline',axis=1,inplace=True)

df=pd.concat([categorical,Airline,source,destination,df[continuous_col]],axis=1)

df.head()

def plot(data,col):
    fig,(ax1,ax2)=plt.subplots(2,1)
    sns.distplot(data[col],ax=ax1)
    sns.boxplot(data[col],ax=ax2)

plot(df,'Price')

"""###Removing the outliers"""

df['Price']=np.where(df['Price']>=40000,df['Price'].median(),df['Price'])

plot(df,'Price')

"""###Generating the predictor and response variables"""

X=df.drop('Price',axis=1)
y=df['Price']

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.20,random_state=188)

X_train

from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
def predict(ml_model):
    print('Model is: {}'.format(ml_model))
    model= ml_model.fit(X_train,y_train)
    print("Training score: {}".format(model.score(X_train,y_train)))
    predictions = model.predict(X_test)
    r2score=r2_score(y_test,predictions) 
    print("R2 score is: {}".format(r2score))
          
    print('Mean Absolute Error:{}'.format(mean_absolute_error(y_test,predictions)))
    print('Mean Sqaured Error:{}'.format(mean_squared_error(y_test,predictions)))
    print('Root Mean Sqauared Error:{}'.format(np.sqrt(mean_squared_error(y_test,predictions))))
     
    sns.distplot(y_test-predictions)

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor,RandomForestRegressor
from sklearn.svm import SVR

predict(RandomForestRegressor())

predict(LogisticRegression())

predict(KNeighborsRegressor())

predict(DecisionTreeRegressor())

predict(SVR())

predict(GradientBoostingRegressor())

import xgboost as xgb
xg_reg=xgb.XGBRegressor()

xg_reg.fit(X_train.values,y_train.values)
pred=xg_reg.predict(X_test.values)
r2_score(y_test.values,pred)

"""###Logistic Regression and KNearest Neighbors give very low r2 scores.
###So there is no point in tuning their hyperparameters

###Feature Selection
"""

from sklearn.feature_selection import mutual_info_classif

mutual_info_classif(X_train,y_train)

fs=pd.DataFrame(mutual_info_classif(X_train,y_train),index=X_train.columns)

fs

fs.columns=['important_features']
fs.sort_values(by='important_features',ascending=False)

"""###We can drop the features with values less than 0.5

"""

X_train_fs=X_train.drop(['Delhi','New Delhi','SpiceJet','Hyderabad','Mumbai','Vistara','Chennai','Kolkata','GoAir','Vistara Premium economy','Multiple carriers Premium economy','Trujet','Jet Airways Business'],axis=1)
X_test_fs=X_test.drop(['Delhi','New Delhi','SpiceJet','Hyderabad','Mumbai','Vistara','Chennai','Kolkata','GoAir','Vistara Premium economy','Multiple carriers Premium economy','Trujet','Jet Airways Business'],axis=1)

X_train_fs

X_test_fs

def pipeline_fs(ml_model):
    print('Model is: {}'.format(ml_model))
    model= ml_model.fit(X_train_fs,y_train)
    print("Training score: {}".format(model.score(X_train_fs,y_train)))
    predictions = model.predict(X_test_fs)
    r2score=r2_score(y_test,predictions) 
    print("R2 score is: {}".format(r2score))
          
    print('Mean Absolute Error:{}'.format(mean_absolute_error(y_test,predictions)))
    print('Mean Sqaured Error:{}'.format(mean_squared_error(y_test,predictions)))
    print('Root Mean Sqauared Error:{}'.format(np.sqrt(mean_squared_error(y_test,predictions))))
     
    sns.distplot(y_test-predictions)

pipeline_fs(RandomForestRegressor())

pipeline_fs(KNeighborsRegressor())

pipeline_fs(DecisionTreeRegressor())

"""###Using XGBoosts DMatrix which will convert the dataset into a data structure known as DMatrix that XGBoost supports and gives its acclaimed performance and efficiency gains."""

import xgboost as xgb

data_dmatrix = xgb.DMatrix(data=X_train_fs,label=y_train)
xg_reg=xgb.XGBRegressor(max_depth=7)

xg_reg.fit(X_train_fs.values,y_train.values)

preds=xg_reg.predict(X_test_fs.values)

r2_score(y_test,preds)

"""###We can see that after the removal of the features the r2score almost remains the same for Random Forest Regressor, Decision Tree Regressor,K Nearest Neighbors and Gradient Boosting but their is a slight increase of r2score in XGBRegressor after the least usable features are dropped"""