function getRecentData() {
    let loc = $('#loc').find(":selected").val();
    console.log(loc);
    $.ajax({
      url: `http://localhost:3000/api/weather`,
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ loc: loc }),
      
      success: function (data) {

        // console.log(data.result['temp_max (⁰C)','humidity_min (%)']) 
        document.getElementById('tm').innerHTML="Temperature: " + data.result['temp_max (⁰C)'] +"⁰C"
        document.getElementById('hu').innerHTML="Humidity: "+data.result['humidity_min (%)'] + " %"
        document.getElementById('ws').innerHTML="Wind Speed: "+data.result['wind_speed_max (Kmph)'] +" Kmph"
        
      },
    })
  }
  
  $(document).ready(()=>{
    setInterval(getRecentData,500);
  })