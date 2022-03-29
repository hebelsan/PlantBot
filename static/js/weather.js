function updateWeather() {
    console.log("updating weather..")
    fetch('/weather', { method: 'GET' })
        .then(response=>response.json())
        .then(data=>{
            document.getElementById('temp_online').textContent = `${data.tempOnline} °C`;
            document.getElementById('hum_online').textContent = `${data.humOnline} %`;
            document.getElementById('press_online').textContent = `${data.pressOnline} hPa`;

            document.getElementById('temp_online').textContent = `${data.tempOnline} °C`;
            document.getElementById('hum_online').textContent = `${data.humOnline} %`;
            document.getElementById('press_online').textContent = `${data.pressOnline} hPa`;
        })
        .catch((err) => { console.log(err); });
}

setInterval(updateWeather, 60*2*1000);