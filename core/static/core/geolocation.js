 // Try HTML5 geolocation.
 if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(function(position) {
    var lat = document.getElementById('latitude');
    var lon = document.getElementById('longitude');
    lat.value = position.coords.latitude;
    lon.value = position.coords.longitude;
  });
} else {
  // Browser doesn't support Geolocation
  handleLocationError(false, infoWindow, map.getCenter());
}