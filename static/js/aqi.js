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
        document.getElementById('aqi').innerHTML=data.result['AQI']
        // document.getElementById('hu').innerHTML=data.result['humidity_min (%)']
        // document.getElementById('ws').innerHTML=data.result['wind_speed_max (Kmph)']
        
      },
    })
  }
  
  $(document).ready(()=>{
    setInterval(getRecentData,1000);
  })