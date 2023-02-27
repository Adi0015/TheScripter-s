function getRecentData() {
    let loc = $('#loc').find(":selected").val();
    console.log(loc);
    $.ajax({
      url: `http://localhost:8080/api/aqi`,
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ loc: loc }),
      
      success: function (data) {
        
        // console.log(data.result['temp_max (⁰C)','humidity_min (%)']) 
        document.getElementById('aqi').innerHTML="AQI"+" "+data.result['AQI']
        document.getElementById('pm10').innerHTML="PM10"+" "+data.result['PM10'] 
        document.getElementById('pm25').innerHTML="PM2.5"+" "+data.result['PM25'] 
        document.getElementById('no2').innerHTML="NO2"+" "+data.result['NO2'] 
        document.getElementById('so2').innerHTML="SO2"+" "+data.result['SO2'] 
         
        // document.getElementById('pollutant').innerHTML="Major Pollutant " + data.result['Main Pollutant'] + " : " +data.result['value']
        
        // document.getElementById('hu').innerHTML=data.result['humidity_min (%)']
        // document.getElementById('ws').innerHTML=data.result['wind_speed_max (Kmph)']
        },
    })
  }
  
  $(document).ready(()=>{
    setInterval(getRecentData,1000);
  })