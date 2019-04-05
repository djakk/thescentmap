var mymap = L.map('mapid').setView([51.505, -0.09], 13);

L.tileLayer('map/{z}/{x}/{y}.png', {
    maxZoom: 18
}).addTo(mymap);
