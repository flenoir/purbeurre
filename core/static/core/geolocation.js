  // Try HTML5 geolocation.
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      sessionStorage.setItem('lat', position.coords.latitude);
      sessionStorage.setItem('lon', position.coords.longitude);
    });
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, map.getCenter());
  }
