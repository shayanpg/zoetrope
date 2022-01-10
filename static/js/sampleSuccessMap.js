function initMap() {
  var polyCoords = JSON.parse(document.getElementById('neighborhood_def').innerHTML);

  // let centerLatVals = [];
  // let centerLngVals = [];
  // for (let i = 0; i < polyCoords.length; i++) {
  //   centerLatVals.push(polyCoords[i]["lat"]);
  //   centerLngVals.push(polyCoords[i]["lng"]);
  // }
  // var centerLat = Math.min(centerLatVals) + Math.max(centerLatVals) / 2;
  // var centerLng = Math.min(centerLngVals) + Math.max(centerLngVals) / 2;

  var centerLat = 0;
  var centerLng = 0;
  for (let i = 0; i < polyCoords.length; i++) {
    centerLat += polyCoords[i]["lat"];
    centerLng += polyCoords[i]["lng"];
  }
  centerLat = centerLat / polyCoords.length;
  centerLng = centerLng / polyCoords.length;

  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15, //try something like (rightlat-leftlat) + (toplat-bottomlat) all * some constant to make it reasonable scale
    center: { lat: centerLat, lng: centerLng },
    mapTypeId: "terrain",
  });

  var sampleCoords = JSON.parse(document.getElementById('sampled_points').innerHTML);
  var fillOp = 0.35;
  document.getElementById('test').innerHTML = "HELLO";
  if (sampleCoords.length > 0) {
    fillOp = 0.1;
    for (let i = 0; i < sampleCoords.length; i++) {
      new google.maps.Marker({ position: sampleCoords[i], map });
    }
  }
  // Construct the polygon.
  const poly = new google.maps.Polygon({
    // paths: triangleCoords,
    paths: polyCoords,
    strokeColor: "#687890",
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: "#687890",
    fillOpacity: fillOp,
  });

  poly.setMap(map);
  // new google.maps.Marker({ position: { lat: centerLat, lng: centerLng }, map });
}

// function succMap() {
//   initMap();
// }
