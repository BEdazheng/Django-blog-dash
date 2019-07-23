from .models import Forecast
import pandas as pd

def from_csv_to_db(f):
    df = pd.read_csv(f)
    print('Im storing in database')
    for i in range(df.shape[0]):
        #yhat,yhat_lower,yhat_upper,y,anomaly,index,pred_date,indicator
        Forecast.objects.create(
                    timestamp=df.iloc[i]['ds'],
                    y = df.iloc[i]['y'],
                    yhat = df.iloc[i]['yhat'],
                    yhat_lower = df.iloc[i]['yhat_lower'],
                    yhat_upper = df.iloc[i]['yhat_upper'],
                    anomaly = df.iloc[i]['anomaly'],
                    pred_date = df.iloc[i]['pred_date'],
                    location = df.iloc[i]['index'],
                    indicator = df.iloc[i]['indicator'],
                )