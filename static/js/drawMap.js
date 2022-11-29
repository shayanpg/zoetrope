// This example requires the Drawing library. Include the libraries=drawing
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=drawing">
function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    center: {lat: 37.873103, lng: -122.259420},
    zoom: 8,
    mapTypeId: google.maps.MapTypeId.HYBRID,
    gestureHandling: "greedy",
  });
  const drawingManager = new google.maps.drawing.DrawingManager({
    drawingMode: google.maps.drawing.OverlayType.POLYGON,
    drawingControl: true,
    drawingControlOptions: {
      position: google.maps.ControlPosition.TOP_CENTER,
      drawingModes: [
        google.maps.drawing.OverlayType.POLYGON,
      ],
    },
    markerOptions: {
      icon: "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png",
    },
    circleOptions: {
      fillColor: "#ffff00",
      fillOpacity: 1,
      strokeWeight: 5,
      clickable: false,
      editable: true,
      zIndex: 1,
    },
  });

  google.maps.event.addListener(drawingManager, 'polygoncomplete', function(polygon) {
    var path = polygon.getPath().getArray();
    document.getElementById('newpath').value = path;
  });

  drawingManager.setMap(map);

  document.getElementById("api_failure").innerHTML = "";
}
