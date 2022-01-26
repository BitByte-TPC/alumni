$(document).ready(function () {
    $('html, body').animate({
        scrollTop: $('#map').offset().top-58.85
    }, 'slow');
})

function resetZoom() {
    map.setView([22.3511148, 78.6677428], 2);
}

var icon = new L.Icon({
    iconUrl: '/static/geolocation/point.png',
    iconAnchor: [12.5, 25]
})

var map = L.map('map', {
    'center': [22.3511148, 78.6677428],
    'zoom': 2,
    'minZoom': 2,
    'maxZoom': 16,
    'maxBounds': [
        [90, -180],
        [-90, 180]
    ]
})

map.zoomControl.setPosition('topright');
L.easyButton('fa-globe',
             function() {
                 resetZoom()
             },
            {position: 'topright',
            title: 'Reset the Zoom'}
             ).addTo(map);

map.on('popupopen', function (e) {
    map.setMaxBounds(null);
});
map.on('popupclose', function (e) {
    map.setMaxBounds([
        [90, -180],
        [-90, 180]
    ]);
});

var layer = new L.StamenTileLayer("toner-lite")
map.addLayer(layer)

var markers = new L.markerClusterGroup({
    showCoverageOnHover: false,
    chunkedLoading: true,
    animateAddingMarkers: true,
    iconCreateFunction: function(cluster) {
		var count = 0;
        cluster.getAllChildMarkers().forEach(function(val){
            count += val.options.count;
        });
        var digits = (count + '').length;
        return L.divIcon({
            html: '<div title="' + count + '""><span class="custom-cluster">' + (count) + '</span></div>',
            className: 'marker-cluster-map digits-' + digits,
            iconSize: null
        })
    }
})
data.forEach(item => {
    var lat = item.lat
    var lon = item.lon
    markers.addLayer(L.marker([lat, lon],{
        icon: icon,
        count: item.count
    }).bindTooltip(item.title.toString())
    .bindPopup('<div class="text-center">Meet '+item.count.toString()+' alumni in '+item.title.toString()+'<br><a href="/members/mapsearch/?search='+encodeURIComponent(item.title.toString())+'"><i class="fa fa-search mt-2"/></a></div>'))
})

map.addLayer(markers)