$(document).ready(function () {
    $(".text").textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },
    });
    //siri
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 640,
        height: 200,
        style: "ios9",
        amplitutde: "1",
        speed: "0.30",
        autostart: true
    });
    $(".siri-message").textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },
    });
    //mic button click
    $("#MicBtn").click(function (e) {
        eel.playmicsound()
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()();
    });
    function doc_keyUp(e) {
        
        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound()
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);
});
// Weather Screen Controls
function showWeatherScreen() {
    document.getElementById('weather-screen').style.display = 'block';
    // Optionally fetch current location weather automatically
    // fetchCurrentLocationWeather();
}

function hideWeatherScreen() {
    document.getElementById('weather-screen').style.display = 'none';
}

// Fetch weather data
async function fetchWeather() {
    const city = document.getElementById('weather-location').value.trim();
    if (!city) {
        alert('Please enter a city name');
        return;
    }
    
    try {
        // Show loading state
        document.getElementById('weather-city').textContent = "Loading...";
        document.getElementById('weather-description').textContent = "";
        
        // Call Python backend through Eel
        const weather = await eel.get_weather(city)();
        
        if (weather.error) {
            throw new Error(weather.error);
        }
        
        // Update UI with weather data
        updateWeatherUI(weather);
        
    } catch (error) {
        document.getElementById('weather-city').textContent = "Error";
        document.getElementById('weather-description').textContent = error.message;
        console.error("Weather error:", error);
    }
}

function updateWeatherUI(weather) {
    document.getElementById('weather-city').textContent = weather.city;
    document.getElementById('weather-temperature').textContent = Math.round(weather.temp);
    document.getElementById('weather-description').textContent = weather.desc;
    document.getElementById('weather-humidity').textContent = `${weather.humidity}%`;
    document.getElementById('weather-wind').textContent = `${Math.round(weather.wind * 3.6)} km/h`;
    document.getElementById('weather-pressure').textContent = `${weather.pressure} hPa`;
    
    // Set weather icon
    const iconClass = getWeatherIconClass(weather.icon);
    document.getElementById('weather-icon').innerHTML = `<i class="wi ${iconClass}"></i>`;
    
    // Set dynamic background
    const bg = document.getElementById('weather-background');
    bg.className = 'weather-bg ' + getWeatherBgClass(weather.icon, weather.desc.toLowerCase());
}

// Helper functions
function getWeatherIconClass(iconCode) {
    const iconMap = {
        '01d': 'wi-day-sunny',
        '01n': 'wi-night-clear',
        '02d': 'wi-day-cloudy',
        '02n': 'wi-night-alt-cloudy',
        '03d': 'wi-cloud',
        '03n': 'wi-cloud',
        '04d': 'wi-cloudy',
        '04n': 'wi-cloudy',
        '09d': 'wi-rain',
        '09n': 'wi-rain',
        '10d': 'wi-day-rain',
        '10n': 'wi-night-alt-rain',
        '11d': 'wi-thunderstorm',
        '11n': 'wi-thunderstorm',
        '13d': 'wi-snow',
        '13n': 'wi-snow',
        '50d': 'wi-fog',
        '50n': 'wi-fog'
    };
    return iconMap[iconCode] || 'wi-day-sunny';
}

function getWeatherBgClass(iconCode, description) {
    if (iconCode.includes('01')) return 'sunny';
    if (iconCode.includes('02') || iconCode.includes('03') || iconCode.includes('04')) return 'cloudy';
    if (iconCode.includes('09') || iconCode.includes('10') || description.includes('rain')) return 'rainy';
    if (iconCode.includes('13') || description.includes('snow')) return 'snowy';
    return 'sunny'; // default
}

// Optional: Fetch weather on Enter key press
document.getElementById('weather-location').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        fetchWeather();
    }
});