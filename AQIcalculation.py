
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
    
    aqi_values = [aqi_so2, aqi_no2, aqi_pm25, aqi_pm10]
    pollutant_concs = [so2_conc, no2_conc, pm25_conc, pm10_conc]
    max_aqi = max(aqi_values)
    max_pollutant_conc = pollutant_concs[aqi_values.index(max_aqi)]
    max_pollutant = ""
    if aqi_values.index(max_aqi) == 0:
        max_pollutant = "SO2"
    elif aqi_values.index(max_aqi) == 1:
        max_pollutant = "NO2"
    elif aqi_values.index(max_aqi) == 2:
        max_pollutant = "PM2.5"
    elif aqi_values.index(max_aqi) == 3:
        max_pollutant = "PM10"
    # print(aqi_pm10,aqi_pm25,pm10_conc)
    aqi = {'AQI':max_aqi, "Main pollutant":max_pollutant,"value": max_pollutant_conc} 
    all = {"PM10" : pm10_conc,"PM2.5":pm25_conc,"NO2":no2_conc,"SO2":so2_conc} 
    return aqi,all


def calculate_aqi_pollutant(conc, pollutant):
# Calculate AQI for each pollutant

# Define the AQI breakpoints and corresponding values for each pollutant
# Define the AQI breakpoints and corresponding values for each pollutant
    if pollutant == "SO2":
        breakpoints = [0, 40, 80, 380, 800, 1600]
        aqi_values = 	[0, 50, 100, 200, 300, 400, 500]
    elif pollutant == "O3":
        breakpoints = 	[0, 50, 100, 168, 208, 748]
        aqi_values = [0, 50, 100, 150, 200, 300, 400]
    elif pollutant == "NO2":
        breakpoints = [0, 40, 80, 180, 280, 400]
        aqi_values = [0, 50, 100, 200, 300, 400, 500]
    elif pollutant == "PM10":
        breakpoints = [0, 50, 100, 250, 350, 430]
        aqi_values = [0, 50, 100, 200, 300, 400, 500]
    elif pollutant == "PM2.5":
        breakpoints = [0, 30, 60, 90, 120, 250, 350, 430]
        aqi_values = [0, 50, 100, 200, 300, 400, 500]
    elif pollutant == "NH3":
        breakpoints = [0, 200, 400, 800, 1200, 1800]
        aqi_values = [0, 50, 100, 200, 300, 400, 500]
    
    
    
    
    # if pollutant == "SO2":
    #     breakpoints = 	[0, 20,40, 80, 160,400,600]
    #     aqi_values = 	[0, 50, 100 , 150, 200, 300, 500]
    # elif pollutant == "O3":
    #     breakpoints = 		[0, 20,50,100,200,400,600]
    #     aqi_values = [0, 50, 100 , 150, 200, 300, 500]
    # elif pollutant == "NO2":
    #     breakpoints = [0, 20,40, 80, 160,400,600]
    #     aqi_values = [0, 50, 100 , 150, 200, 300, 500]
    # elif pollutant == "PM10":
    #     breakpoints = [0,30,60,100,200,300,400 ]
    #     aqi_values = [0, 50, 100 , 150, 200, 300, 500]
    # elif pollutant == "PM2.5":
    #     breakpoints = [0, 20,40,60,100,200,300]
    #     aqi_values = [0, 50, 100 , 150, 200, 300, 500]
    # elif pollutant == "NH3":
    #     breakpoints = [0, 200, 400, 800, 1200, 1800]
    #     aqi_values = [0, 50, 100 , 150, 200, 300, 500]  
        
        
        
        
    # if pollutant == "SO2":
    #     breakpoints = 	[0, 40, 80, 380, 800, 1600]
    #     aqi_values = 	[0, 50, 100, 150, 200, 300, 400]
    # elif pollutant == "O3":
    #     breakpoints = 	[0, 54, 70, 85, 105, 200, 405]
    #     aqi_values = [0, 50, 100, 150, 200, 300, 400]
    # elif pollutant == "NO2":
    #     breakpoints = 	[0, 40, 80, 180, 280, 400]
    #     aqi_values = [0, 50, 100, 150, 200, 300, 400]
    # elif pollutant == "PM10":
    #     breakpoints = 	[0, 54, 154, 254, 354, 424]
    #     aqi_values = [0, 50, 100, 150, 200, 300, 400]
    # elif pollutant == "PM2.5":
    #     breakpoints = [0, 12, 35.4, 55.4, 150.4, 250.4, 350.4, 500.4]
    #     aqi_values = [0, 50, 100, 150, 200, 300, 400]
    # elif pollutant == "NH3":
    #     breakpoints = [0, 200, 400, 800, 1200, 1800]
    #     aqi_values = [0, 50, 100, 150, 200, 300, 400] 
        
        
        
        
       
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