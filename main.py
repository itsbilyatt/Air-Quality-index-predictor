####################################################################################
# import required library
####################################################################################

import pandas as pd
import numpy as np
import pickle
import math
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score
from sklearn import metrics

# import data set and preprocess it for model building
df = pd.read_excel(r"data/AirData.xlsm",header=0)

# remove unnecessary columns
df.drop(['agency'],axis=1,inplace=True)
df.drop(["stn_code"],axis=1,inplace=True)
df.drop(['date'],axis=1,inplace=True)
df.drop(['sampling_date'],axis=1,inplace=True)
df.drop(['location_monitoring_station'],axis=1,inplace=True)

df["location"]=df["location"].fillna(df['location'].mode()[0])
df["type"]=df["type"].fillna(df['type'].mode()[0])
df.fillna(0,inplace=True)
df.fillna(0,inplace=True)

def calculate_si(so2):
    si=0
    if (so2<=40):
         si= so2*(50/40)
    if (so2>40 and so2<=80):
         si=50+(so2-40)*(50/40)
    if (so2>80 and so2<=380):
         si=100+(so2-80)*(100/300)
    if (so2>380 and so2<=800):
         si=200+(so2-380)*(100/800)
    if (so2>800 and so2<=1600):
         si=300+(so2-800)*(100/800)
    if (so2>1600):
         si=400+(so2-1600)*(100/800)
    return si
df["Soi"]=df["so2"].apply(calculate_si)
soi_data=df[["so2","Soi"]]

def calculate_ni(no2):
    ni=0
    if(no2<=40):
         ni=no2*50/40
    elif(no2>40 and no2<=80):
         ni=50+(no2-14)*(50/40)
    elif(no2>80 and no2<=180):
         ni=100+(no2-80)*(100/100)
    elif(no2>180 and no2<=280):
         ni=200+(no2-180)*(100/100)
    elif(no2>280 and no2<=400):
         ni=300+(no2-280)*(100/120)
    else:
         ni=400+(no2-400)*(100/120)
    return ni
df["Noi"]=df["no2"].apply(calculate_ni)

def calculate_(rspm):
    rpi=0
    if(rpi<=30):
         rpi=rpi*50/30
    elif(rpi>30 and rpi<=60):
         rpi=50+(rpi-30)*50/30
    elif(rpi>60 and rpi<=90):
         rpi=100+(rpi-60)*100/30
    elif(rpi>90 and rpi<=120):
         rpi=200+(rpi-90)*100/30
    elif(rpi>120 and rpi<=250):
         rpi=300+(rpi-120)*(100/130)
    else:
         rpi=400+(rpi-250)*(100/130)
    return rpi
df["Rspmi"]=df["rspm"].apply(calculate_)

def calculate_spi(spm):
    spi=0
    if(spm<=50):
         spi=spm
    if(spm<50 and spm<=100):
         spi=spm
    elif(spm>100 and spm<=250):
         spi= 100+(spm-100)*(100/150)
    elif(spm>250 and spm<=350):
         spi=200+(spm-250)
    elif(spm>350 and spm<=450):
         spi=300+(spm-350)*(100/80)
    else:
         spi=400+(spm-430)*(100/80)
    return spi
df["Spmi"]=df["spm"].apply(calculate_spi)

def cal_Pmi(pm2_5):
    pmi=0
    if pm2_5<=30:
        pmi=pm2_5*50/30
    elif pm2_5<=60:
        pmi=50+(pm2_5-30)*50/30
    elif pm2_5<=90:
        pmi=100+(pm2_5-60)*100/30
    elif pm2_5<=120:
        pmi=200+(pm2_5-90)*100/30
    elif pm2_5<=250:
        pmi=300+(pm2_5-120)*100/130
    elif pm2_5>250:
        pmi=400+(pm2_5-250)*(100/130)

df["Pmi"]=df["pm2_5"].apply(cal_Pmi)
def calculate_aqi(si,ni,spi,rpi):
    aqi=0
    if(si>ni and si>spi and si>rpi):
         aqi=si
    if(spi>si and spi>ni and spi>rpi):
         aqi=spi
    if(ni>si and ni>spi and ni>rpi):
         aqi=ni
    if(rpi>si and rpi>ni and rpi>spi):
         aqi=rpi
    return aqi
df["AQI"]=df.apply(lambda x:calculate_aqi(x["Soi"],x["Noi"],x["Rspmi"],x["Spmi"]),axis=1)
aqi_data=df[["state","Soi","Noi","Rspmi","Spmi","AQI"]]


def Aqi_analysis(x):
    if x<=50:
        return "Good"
    elif x>50 and x<=100:
        return "Moderate"
    elif x>100 and x<=200:
        return "Poor"
    elif x>200 and x<=300:
        return "Unhealthy"
    elif x>400:
        return "Hazardous"
df["Aqi_range"]=df["AQI"].apply(Aqi_analysis)
df.head()

model = LinearRegression()
x=df[["Soi","Noi","Rspmi","Spmi"]]
y=df["AQI"]



x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=70)
print(x_train.shape,x_test.shape,y_train.shape,y_test.shape)

model.fit(x_train,y_train)

train_pred=model.predict(x_train)
test_pred=model.predict(x_test)

# RMSE_train=np.sqrt(metrics.mean_squared_error(y_train,train_pred))
# RMSE_test=np.sqrt(metrics.mean_squared_error(y_test,test_pred))
# print("RMSE TrainingData=",str(RMSE_train))
# print("RMSE TestData=",str(RMSE_test))
# print("_"*50)
print("RSqured value on train:",model.score(x_train,y_train))
print("RSqured value on test:",model.score(x_test,y_test))

model.predict([[6.000,21.750,0.0,0.0]])

pickle.dump(model, open('model.pkl', 'wb'))
