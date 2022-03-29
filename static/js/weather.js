function updateWeather() {
    console.log("updating weather..")
    fetch('/weather', { method: 'GET' })
        .then(response=>response.json())
        .then(data=>{ 
            document.getElementById('tmp_online').textContent = `${data.temp} °C`;
            document.getElementById('hum_online').textContent = `${data.humidity} %`;
            document.getElementById('press_online').textContent = `${data.pressure} hPa`;
        })
        .catch((err) => { console.log(err); });
}

setInterval(updateWeather, 60*2*1000);