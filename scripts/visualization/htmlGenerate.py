
import csv
import os.path

def readFile(relativePath):
    ''' Read csv file and return generator of information'''
    with open(relativePath) as csvfile:
        reader = csv.DictReader(csvfile)
        # Return information (as list to remove generator and not able to call)

        return list(reader)

craftCsv = readFile('../../data/Spacecrafts.csv')

craftNames = []
for dictionary in craftCsv:
    craftNames.append(dictionary["Spacecraft"])

print craftNames

html_str = """
<html>
<header>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.min.js"></script>

</header>

<body>
<div style= "width:500px; height:500px;">
<canvas id="SpacecraftWeight"></canvas>
</div>

<script>
var ctx = document.getElementById("SpacecraftWeight").getContext('2d');
var SpacecraftWeight = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["Cygnus", "Progress", "Kounotori", "Dragon"],
        ,datasets: [{
            label: 'Weight',
            data: [2000, 2400, 5200, 6000],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
</script>

<div style= "width:500px; height:500px;">
<canvas id="SpacecraftVolume"></canvas>
</div>

<script>
var ctx = document.getElementById("SpacecraftVolume").getContext('2d');
var SpacecraftVolume = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["Cygnus", "Progress", "Kounotori", "Dragon"],
        datasets: [{
            label: 'Volume',
            data: [18.9, 7.6, 14, 10],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
</script>
"""

html_str += """
<div style= "width:500px; height:500px;">
<canvas id="parcelScatter"></canvas>
</div>
<script>
var ctx = document.getElementById("parcelScatter").getContext('2d');
var scatterChart = new Chart(ctx, {
    type: 'scatter',
    data: {
        labels: ["Cygnus", "Progress", "Kounotori", "Dragon"],
        datasets: [{
            label: 'Scatter Dataset',
            data: [{
                x: -10,
                y: 0
            }, {
                x: 0,
                y: 10
            }, {
                x: 10,
                y: 5
            }]
        }]
    },
    options: {
        scales: {
            xAxes: [{
                type: 'linear',
                position: 'bottom'
            }]
        }
    }
});
</script>
</body>

</html>
"""

Html_file= open("filename.html","w")
Html_file.write(html_str)
Html_file.close()
