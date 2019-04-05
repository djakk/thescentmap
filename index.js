function load_map()
{
    var mymap = L.map('mapid').setView([0.0, 0.0], 13);
    
    L.tileLayer('/map/{z}/{x}/{y}.png', {
      maxZoom: 18
    }).addTo(mymap);
}
