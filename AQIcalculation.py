
import math


def calculate_aqi(data):
    # Calculate AQI for each pollutant
    no2_conc = data['list'][0]['components']['no2']
    O3_conc = data['list'][0]['components']['o3']
    pm25_conc = data['list'][0]['components']['pm2_5']
    pm10_conc = data['list'][0]['components']['pm10']
    so2_conc = data['list'][0]['components']['so2']
    nh3_conc = data['list'][0]['components']['nh3']
    
    aqi_so2 = calculate_aqi_pollutant(so2_conc, "SO2")
    aqi_O3 = calculate_aqi_pollutant(O3_conc, "O3")
    aqi_no2 = calculate_aqi_pollutant(no2_conc, "NO2")
    aqi_pm10 = calculate_aqi_pollutant(pm10_conc, "PM10")
    aqi_pm25 = calculate_aqi_pollutant(pm25_conc, "PM2.5")
    aqi_nh3 = calculate_aqi_pollutant(nh3_conc, "NH3")
    
    
    

    # Determine the overall AQI by taking the maximum AQI value
    aqi_v= max(aqi_so2, aqi_O3, aqi_no2, aqi_pm10, aqi_pm25, aqi_nh3)
    aqi = {'AQI':aqi_v,'NO2':no2_conc,'O3': O3_conc,'PM25': pm25_conc,'PM10':pm10_conc,'SO2': so2_conc,"NH3":nh3_conc}
    # aqi = statistics.mea(aqi)
    return aqi


def calculate_aqi_pollutant(conc, pollutant):
# Calculate AQI for each pollutant

# Define the AQI breakpoints and corresponding values for each pollutant
    if pollutant == "SO2":
        breakpoints = [0, 35, 75, 185, 304, 604, 804, 1004]
        aqi_values = [0, 50, 100, 150, 200, 300, 400, 500]
    elif pollutant == "O3":
        breakpoints = [0, 54, 70, 85, 105, 200, 404, 504]
        aqi_values = [0, 50, 100, 150, 200, 300, 400, 500]
    elif pollutant == "NO2":
        breakpoints = [0, 53, 100, 360, 649, 1249, 1649, 2049]
        aqi_values = [0, 50, 100, 150, 200, 300, 400, 500]
    elif pollutant == "PM10":
        breakpoints = [0, 54, 154, 254, 354, 424, 504, 604]
        aqi_values = [0, 50, 100, 150, 200, 300, 400, 500]
    elif pollutant == "PM2.5":
        breakpoints = [0, 12, 35.4, 55.4, 150.4, 250.4, 350.4, 500.4]
        aqi_values = [0, 50, 100, 150, 200, 300, 400, 500]
    elif pollutant == "NH3":
        breakpoints = [0, 53, 100, 200, 400, 800, 1200, 1800]
        aqi_values = [0, 50, 100, 150, 200, 300, 400, 500]
    else:
        raise ValueError("Invalid pollutant type")

# Calculate the AQI for the given concentration value
    if conc <= breakpoints[0]:
        aqi = 0
    elif conc > breakpoints[-1]:
        aqi = 500
    else:
        for i in range(len(breakpoints)-1):
            if conc > breakpoints[i] and conc <= breakpoints[i+1]:
                aqi = (aqi_values[i+1] - aqi_values[i]) / (breakpoints[i+1] -  breakpoints[i]) * (conc - breakpoints[i]) + aqi_values[i]

    return math.ceil(aqi) if (aqi - math.floor(aqi)) >= 0.5 else math.floor(aqi)