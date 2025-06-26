// Clock functionality
function updateClock() {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const seconds = now.getSeconds();

    // Calculate angles
    const secondDegrees = (seconds / 60) * 360;
    const minuteDegrees = ((minutes + seconds/60) / 60) * 360;
    const hourDegrees = ((hours % 12 + minutes/60) / 12) * 360;

    // Update clock hands
    document.getElementById('second').style.transform = `rotate(${secondDegrees}deg)`;
    document.getElementById('minute').style.transform = `rotate(${minuteDegrees}deg)`;
    document.getElementById('hour').style.transform = `rotate(${hourDegrees}deg)`;
}

// Update clock every second
setInterval(updateClock, 1000);
updateClock(); // Initial call

// Function to fetch sensor data from Raspberry Pi
async function fetchSensorData() {
    try {
        const response = await fetch('http://<pi_ip:5000>/sensor-data');
        const data = await response.json();
        
        // Update temperature
        const tempElement = document.getElementById('temp');
        tempElement.innerHTML = `${data.temperature}°<span class="tempUnit">C</span>`;
	const tempPre = document.getElementById('feelsLike');
	tempPre.innerHTML = `Predicted : ${data.predicted}°C`;
        
        // Update humidity bar
        const humiditySlider = document.getElementById('slider');
        const humidityLevel = document.getElementById('humidityLevel');
        humiditySlider.style.width = `${data.humidity}%`;
        humidityLevel.textContent = `Humidity ${data.humidity}%`;
        
        // Update condition text based on temperature and humidity
        const conditionText = document.getElementById('conditionText');
        updateConditionText(data.temperature, data.humidity);
    } catch (error) {
        console.error('Error fetching sensor data:', error);
    }
}

function updateConditionText(temp, humidity) {
    const conditionText = document.getElementById('conditionText');
    if (temp > 30) {
        conditionText.textContent = "It's quite hot today!";
    } else if (temp < 20) {
        conditionText.textContent = "It's a bit cool today.";
    } else {
        conditionText.textContent = "The temperature is pleasant.";
    }
}

// Fetch sensor data every 30 seconds
setInterval(fetchSensorData, 30000);
fetchSensorData(); // Initial call
