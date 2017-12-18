import csv
import os.path

def readFile(relativePath):
    ''' Read csv file and return generator of information'''
    with open(relativePath) as csvfile:
        reader = csv.DictReader(csvfile)
        # Return information (as list to remove generator and not able to call)

        return list(reader)

parcelCsv = readFile('../../data/CargoList1.csv')

parcelInfo = []
for dictionary in parcelCsv:
    parcelInfo.append((dictionary["parcel_ID"], dictionary["weight (kg)"], dictionary["volume (m^3)"]))

data = []
for dictionary in parcelCsv:
    data.append({"x": dictionary["weight (kg)"], "y": dictionary["volume (m^3)"]})

html_str = """
<html>
<header>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.min.js"></script>

</header>

<body>

<div style= "width:1000px; height:1000px;">
<canvas id="parcelScatter"></canvas>
</div>
<script>
var ctx = document.getElementById("parcelScatter").getContext('2d');
var scatterChart = new Chart(ctx, {
    type: 'scatter',
    data: {
        datasets: [{
            label: 'Scatterplot Parcel List 1',
            fill: false,
            showLine: false,
            pointBackgroundColor: 'rgba(122, 172, 255,0.5)',
            pointBorderColor: 'rgba(0, 97, 255,1)',
            pointBorderWidth: 2,
            data: """ + str(data) + """
        }]
    },
    options: {
        scales: {
            xAxes: [{
                type: 'linear',
                position: 'bottom',
                display: true,
                labelString: 'probability'
            }]

        }
    }
});
</script>
</body>

</html>
"""

Html_file= open("parcelScatter1.html","w")
Html_file.write(html_str)
Html_file.close()
