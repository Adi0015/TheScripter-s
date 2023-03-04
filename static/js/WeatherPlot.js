function updateGraph() {
    var loc = document.getElementById("loc").value;
    var weatherVar = document.getElementById("weatherVar").value;
    console.log(loc);
    $.ajax({
        type: "GET",
        url: "/plot/weather",
        data: {
            loc: loc,
            weatherVar: weatherVar
        },
        success: function(response) {
            var x = response.x;
            var y = response.y;
            var loc = response.loc;
            var weatherVar = response.weatherVar;
            plt(x, y, loc, weatherVar);
        },
        error: function() {
            alert("Error updating graph.");
        }
    });
}
setInterval(updateGraph, 500);

function plt(x, y, loc, weatherVar) {
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

    // Determine y-axis label based on weather variable
    var yLabel = "";
    if (weatherVar == "MinTemp") {
        yLabel = "Minimum Temperature";
    } else if (weatherVar == "MaxTemp") {
        yLabel = "Maximum Temperature";
    } else if (weatherVar == "Humidity") {
        yLabel = "Humidity";
    } else if (weatherVar == "HeatWaveIndex") {
        yLabel = "Heat Wave Index";
    }

    // Determine trace data based on weather variable
    var traceData = [];
    var traceType = "";
    var traceMode = "";
    var traceFill = "";
    if (weatherVar == "MinTemp") {
        traceData = yFiltered;
        traceType = "scatter";
        traceMode = "lines";
        traceFill = "tozeroy";
    } else if (weatherVar == "MaxTemp") {
        traceData = yFiltered;
        traceType = "scatter";
        traceMode = "lines";
        traceFill = "tozeroy";
    } else if (weatherVar == "Humidity") {
        traceData = yFiltered.map(function(val) {
            return val * 100; // Convert decimal to percentage
        });
        traceType = "scatter";
        traceMode = "lines";
        traceFill = "tozeroy";
    } else if (weatherVar == "HeatWaveIndex") {
        traceData = yFiltered;
        traceType = "bar";
        traceMode = "";
        traceFill = "";
        var markerColors = [];
        for (var i = 0; i < yFiltered.length; i++) {
            if (yFiltered[i] < 1) {
                markerColors.push('rgb(158, 202, 225)');
            } else if (yFiltered[i] < 2) {
                markerColors.push('rgb(107, 174, 214)');
            } else if (yFiltered[i] < 3) {
                markerColors.push('rgb(66, 146, 198)');
            } else if (yFiltered[i] < 4) {
                markerColors.push('rgb(33, 113, 181)');
            } else if (yFiltered[i] < 5) {
                markerColors.push('rgb(8, 81, 156)');
            } else if (yFiltered[i] < 6) {
                markerColors.push('rgb(8, 48, 107)');
            } else {
                markerColors.push('rgb(3, 19, 43)');
            }
        }
 
    }
    
    
    // Create plot trace
    var trace = {
        x: xFiltered,
        y: traceData,
        type: traceType,
        mode: traceMode,
        marker: {
            color: markerColors
        },
        fill: traceFill,
        name: loc + " " + weatherVar,
        line: {
            color: 'rgb(255, 127, 14)',
            width: 3
        },
        fillcolor: 'rgba(255, 127, 14, 0.3)'
    };

    // Create plot layout
    var layout = {
        title: '2023 Weather Forecast',
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
    Plotly.newPlot('Wplot', data, layout);
}
