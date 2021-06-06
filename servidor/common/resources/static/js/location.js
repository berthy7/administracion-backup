const tilesProvider = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
let myMap = L.map('map').setView([-17.783751985640855, -63.181171417236335], 13);
let popup = L.popup();

function init_map() {
    let marker = L.marker([-17.783751985640855, -63.181171417236335], {draggable: true}).addTo(myMap);
    L.tileLayer(tilesProvider, {
        maxZoom: 18,
    }).addTo(myMap);

    marker.on('moveend', e => {
        latitud.value = e.sourceTarget._latlng.lat
        longitud.value = e.sourceTarget._latlng.lng
        $(latitud).parent().addClass('focused')
        $(longitud).parent().addClass('focused')
        onMarkerClick(e.sourceTarget)
    });
}

function onMarkerClick(e) {
    popup.setLatLng(e._latlng).setContent("Ubicación: " + e._latlng.toString()).openOn(myMap);
}
