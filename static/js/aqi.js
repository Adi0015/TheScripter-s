function getRecentData() {
    let loc = $('#loc').find(":selected").val();
    console.log(loc);
    $.ajax({
      url: `http://localhost:3000/api/aqi`,
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ loc: loc }),
      
      success: function (data) {
        
        // console.log(data.result['temp_max (⁰C)','humidity_min (%)']) 
        document.getElementById('aqi').innerHTML="AQI"+" "+data.result['AQI'];
          let aqiValue = parseInt(data.result['AQI']);
          if (aqiValue <= 50) {
            document.getElementById('aqi').style.backgroundColor = '#34A12C';
          } else if (aqiValue <= 100) {
            document.getElementById('aqi').style.backgroundColor = '#D3CC0D';
          } else if (aqiValue <= 200) {
            document.getElementById('aqi').style.backgroundColor = '#EA572A';
          } else if (aqiValue <= 300) {
            document.getElementById('aqi').style.backgroundColor = '#EF4C9F';
          } else if (aqiValue <= 400) {
            document.getElementById('aqi').style.backgroundColor = '#9C5AA5';
          } else {
            document.getElementById('aqi').style.backgroundColor = '#BF202F';
          }
          // Update other tiles here
        
        document.getElementById('pm10').innerHTML="PM10"+": "+data.result['PM10'] 
        document.getElementById('pm25').innerHTML="PM2.5"+": "+data.result['PM2.5'] 
        document.getElementById('no2').innerHTML="NO2"+": "+data.result['NO2'] 
        document.getElementById('so2').innerHTML="SO2"+": "+data.result['SO2'] 
         
        // document.getElementById('pollutant').innerHTML="Major Pollutant " + data.result['Main Pollutant'] + " : " +data.result['value']
        
        // document.getElementById('hu').innerHTML=data.result['humidity_min (%)']
        // document.getElementById('ws').innerHTML=data.result['wind_speed_max (Kmph)']
        },
    })
  }
  
  $(document).ready(()=>{
    setInterval(getRecentData,500);
  })