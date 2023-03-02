function updateGraph() {
    var loc = document.getElementById("loc").value;
    console.log(loc);
    $.ajax({
        type: "GET",
        url: "/plot",
        data: {
            loc: loc
        },
        success: function(response) {
            var x = response.x;
            var y = response.y;
            var loc = response.loc;
            plt(x,y,loc);
        },
        error: function() {
            alert("Error updating graph.");
        }
    });
}
window.onload = () => {
    updateGraph()
}

function plt(x,y,loc){
    var trace = {
        x: x,
        y: y,
        type: 'bar',
        name: loc
    };

    var layout = {
        title: 'Flask Plotly Graph',
        xaxis: {
            title: 'x'
        },
        yaxis: {
            title: 'y'
        }
    };

    var data = [trace];

    Plotly.newPlot('plot', data, layout);
}