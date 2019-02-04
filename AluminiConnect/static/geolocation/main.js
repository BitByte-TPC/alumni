var map = L.map('map',{
    center: [23.1787577,80.0249303],
    zoom: 2
});
var markers = L.markerClusterGroup();

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributor',    
}).addTo(map);


var center = map.getCenter();
for(var i = 0; i < 500 ;i++){
    markers.addLayer(L.marker([center.lat + Math.random(-20,20),center.lng + Math.random(-20,20)]));
}
map.addLayer(markers);