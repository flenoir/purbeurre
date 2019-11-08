  // Try HTML5 geolocation.
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      console.log(pos);
      // $('#coordinates').innerHTML(pos)
      $("#coordinates").text(pos);
      
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
