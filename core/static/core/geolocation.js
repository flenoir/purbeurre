  // Try HTML5 geolocation.
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      var lat = document.getElementById('latitude');
      var lon = document.getElementById('longitude');
      lat.value = position.coords.latitude;
      lon.value = position.coords.longitude;


      console.log(pos);
   
      
    //   geocoder.geocode( { 'location': pos}, function(results, status, infowindow) {
    //   if (status == 'OK') {
    //         console.log(results[0].formatted_address);
    //         infoWindow.setContent('Location found: '+ results[0].formatted_address);
    //         infoWindow.setPosition(pos);
    //         infoWindow.open(map);
    //   } else {
    //   			console.log('Geocode was not successful for the following reason: ' + status);
    //   }
    // });

    //   map.setCenter(pos);
    });
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, map.getCenter());
  }
