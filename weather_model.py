import pandas as pd
import numpy as np
import seaborn as sns
from datetime import date,timedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

def datesForForecast():
    train_end_date = date.today() - timedelta(days=1)
    train_start_date = train_end_date - timedelta(days=672)
    pred_start_date = date.today() + timedelta(days=1)
    pred_end_date = pred_start_date + timedelta(days=183)
    
    return train_end_date,train_start_date,pred_start_date,pred_end_date

# def dataConsistence():
#     dic = {"Adilabad":"{'lon': 78.5, 'lat': 19.5}", 
#             "Nizamabad":"{'lon': 78.25, 'lat': 18.75}",
#             "Warangal":"{'lon': 79.5971, 'lat': 17.9821}",
#             "Karimnagar":"{'lon': 79.1328, 'lat': 18.4348}",
#             "Khammam":"{'lon': 80.3333, 'lat': 17.5}"}
#     latlon = ast.literal_eval(dic[district])
    
#     lat = latlon['lat']
#     lon = latlon['lon']