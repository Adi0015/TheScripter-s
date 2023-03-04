
# Our Solution for T-AIMS Challenge

Academic Grand Challenge on Climate Change

### Problem Statement
To develop solutions that can predict the occurrence of heat waves and the Air Quality Index (AQI) for Tier-2 cities of Telangana. The goal is to come up with innovative and effective ways to mitigate the impact of heat waves and poor air quality on the health and well-being of the residents in these cities. The solutions should be based on data-driven models and take into account various factors such as temperature, humidity, wind speed, and pollution levels.


### Demo




### Our solution
 - > In our project, data for Telangana's Tier 2 cities is fetched and stored in a CSV file. Using this data, we will then undertake data analysis and preprocessing in order to gain insightful information.

- > Using MAPE to assess the model's correctness, we were able to obtain a score that was reasonably low, indicating that the AQI prediction was accurate 

- >  Using maximum temperature data, we also forecasted heat waves. Overall, our approach offers a trustworthy way to anticipate AQI and heat waves in Telangana's Tier 2 cities.

- > Our solution also involves retraining our model every seven days to improve the accuracy of our predictions. To achieve this, we collect current data to update the historical data used to train the model. By doing so, our model can make more accurate predictions based on the most recent data available.




### Our Model

- >  Our project involves the use of ***SARIMAX model***, a powerful time series forecasting model that can take into account both the time component and exogenous variables such as weather data. SARIMAX model allows us to accurately predict the AQI and identify periods of heat waves using historical data and current weather data obtained from APIs.
- > We evaluated the model's accuracy using Mean Absolute Percentage Error (MAPE). Our project also involved predicting heat waves using the temperature data obtained from Open Weather API.
- > Model Accuracy for :
- > Model Workflow 

- > [4d81f26b-8441-4108-99f0-6f4c9b4daa2c](https://user-images.githubusercontent.com/96522398/222914073-2aeec4aa-a9b1-429e-8c27-f6ebff105601.jpg)
    

### Project Features

- Real-time AQI and Pollutants such as PM2.5, PM10, SO2, NO2 

- Real-time Weather with Temperature, Humidity and Wind Speed

- AQI and weather models are retrained every seven days, ensuring that the predictions remain accurate and relevant.

- The project also includes an interactive graph that displays the Predicted AQI data and weather Data for the selected city
### Installation



Clone the repository using the following command:
```bash
git clone https://github.com/Adi0015/TheScripter-s.git
```
Change directory to the project directory:
```bash
cd TheScripter's
```
Activate the virtual environment:
```bash
source env/bin/activate
```
Install the required packages:
```bash
pip install -r requirements.txt
```
Start the application:
```bash
python3 app.py
```
## Screenshots


### Team Members

- [Aditya Gohil](https://github.com/Adi0015)
- [Aman Yevge](https://github.com/amanyevge)
- [Ria Kokate](https://github.com/RiaKokate)
- [Sanika Chaudhari](https://github.com/Sanika0701)

