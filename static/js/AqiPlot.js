function updateGraph() {
    var loc = document.getElementById("loc").value;
    var aqiVar = document.getElementById("aqiVar").value;
    console.log(loc);
    $.ajax({
        type: "GET",
        url: "/plot/aqi",
        data: {
            loc: loc ,
            aqiVar:aqiVar
        },
        success: function(response) {
            var x = response.x;
            var y = response.y;
            var loc = response.loc;
            var aqiVar = response.aqiVar
            plt(x,y,loc,aqiVar);
        },
        error: function() {
            alert("Error updating graph.");
        }
    });
}
setInterval(updateGraph,500);

function plt(x, y, loc,aqiVar) {
    // Get current year
    var currentYear = new Date().getFullYear();
    
    // Filter data for current year
    var xFiltered = [];
    var yFiltered = [];
    for (var i = 0; i < x.length; i++) {
      if (new Date(x[i]).getFullYear() == currentYear) {
        xFiltered.push(x[i]);
        yFiltered.push(y[i]);
      }
    }
    
    var yLabel = "";
    if(aqiVar == "AQI"){
      yLabel = "AQI";
    } else if (aqiVar == "PM2.5"){
      yLabel = "PM2.5";
    } else if (aqiVar == "PM10"){
      yLabel = "PM10";
    } else if (aqiVar == "NO2"){
      yLabel = "NO2";
    } else if (aqiVar == "SO2"){
      yLabel = "SO2";
    } 
    
    
    var traceData = [];
    var traceType = "";
    var traceMode = "";
    var traceFill = "";
    if (aqiVar == "AQI"){
      traceData = yFiltered;
      traceType = "bar";
      traceMode = "";
      traceFill = "";
      var markerColors = [];
        for (var i = 0; i < yFiltered.length; i++) {
            if (yFiltered[i] <= 50) {
                markerColors.push('#34A12C');
            } else if (yFiltered[i] <= 100) {
                markerColors.push('#D3CC0D');
            } else if (yFiltered[i] <= 200) {
                markerColors.push('#EA572A');
            } else if (yFiltered[i] <= 300) {
                markerColors.push('#EF4C9F');
            } else if (yFiltered[i] <= 400) {
                markerColors.push('#9C5AA5');
            } else {
                markerColors.push('#BF202F');
            }
        }
    } else if (aqiVar == "PM2.5"){
      traceData = yFiltered;
      traceType = "scatter";
      traceMode = "lines";
      traceFill = "tozeroy";
    } else if (aqiVar == "PM10"){
      traceData = yFiltered;
      traceType = "scatter";
      traceMode = "lines";
      traceFill = "tozeroy";  
    } else if (aqiVar == "NO2"){
      traceData = yFiltered;
      traceType = "scatter";
      traceMode = "lines";
      traceFill = "tozeroy";
    } else if (aqiVar == "SO2"){
      traceData = yFiltered;
      traceType = "scatter";
      traceMode = "lines";
      traceFill = "tozeroy";
    }
    // Create plot trace
    var trace = {
      x: xFiltered,
      y: traceData,
      type: traceType,
      mode: traceMode,
      name: loc + " " + aqiVar,
      marker:{
        color: markerColors,
      },
      fill: traceFill,
      line: {
        color: 'rgb(255, 127, 14)',
        width: 3
      },
      fillcolor: 'rgba(255, 127, 14, 0.3)'
    };
  
    // Create plot layout
    var layout = {
      title: '2023 AQI Forecast',
      xaxis: {
        title: 'Date'
      },
      yaxis: {
        title: yLabel
      }
    };
  
    // Create plot data array
    var data = [trace];
  
    // Create plot
    Plotly.newPlot('Aplot', data, layout);
  }
  


