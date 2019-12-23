var map = L.map('map', {
    center: [23.1787577, 80.0249303],
    zoom: 2
});
var markers = L.markerClusterGroup();

L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributor',
}).addTo(map);

city.forEach(item => {
    var xhttp = new XMLHttpRequest();

    var city = item.fields.city;
    var url = 'https://nominatim.openstreetmap.org/search?format=json&limit=5&q=' + encodeURIComponent(city);
    xhttp.open("GET", url, true);
    xhttp.send();

    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var res = JSON.parse(this.responseText);
            console.log(res);
            var lat = res[0].lat;
            var lon = res[0].lon;
            markers.addLayer(L.marker([lat, lon]));
        }
    };
});

map.addLayer(markers);


