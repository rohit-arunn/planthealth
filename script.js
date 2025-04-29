window.onload = function() {
    const ctx = document.getElementById('moistureChart').getContext('2d');
    const moistureChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Soil Moisture (%)',
                data: [],
                borderColor: 'green',
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    title: { display: true, text: 'Time' }
                },
                y: {
                    title: { display: true, text: 'Soil Moisture (%)' },
                    min: 0,
                    max: 100
                }
            }
        }
    });

    function updateChart() {
        fetch('/data')
            .then(response => response.json())
            .then(data => {
                console.log("Fetched data:", data);
    
                // Extract just the time part for graph labels
                const timeLabels = data.labels.map(ts => {
                    const date = new Date(ts);
                    return date.toLocaleTimeString(); // returns "HH:MM:SS"
                });
    
                // Set date title above chart
                if (data.labels.length > 0) {
                    const fullDate = new Date(data.labels[data.labels.length - 1]);
                    document.getElementById('dateDisplay').innerText =
                        `${fullDate.toDateString()}`;
                }
    
                // Update chart data
                moistureChart.data.labels = timeLabels;
                moistureChart.data.datasets[0].data = data.moisture;
                moistureChart.update();
            })
            .catch(error => console.error('Error fetching data:', error));
    }
    


    setInterval(updateChart, 5000);
};
