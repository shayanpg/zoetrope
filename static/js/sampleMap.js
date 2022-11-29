function initMap() {
  var polyCoords = JSON.parse(document.getElementById('neighborhood_def').innerHTML);

  var centerLat = 0, centerLng = 0;
  // var latMin = Number.MAX_VALUE, latMax = Number.MIN_VALUE;
  // var lngMin = Number.MAX_VALUE, lngMax = Number.MIN_VALUE;
  for (let i = 0; i < polyCoords.length; i++) {
    var currLat = polyCoords[i]["lat"], currLng = polyCoords[i]["lng"];
    centerLat += currLat;
    // latMin = Math.min(latMin, currLat);
    // latMax = Math.max(latMax, currLat);

    centerLng += currLng;
    // lngMin = Math.min(lngMin, currLng);
    // lngMax = Math.max(lngMax, currLng);
  }
  centerLat = centerLat / polyCoords.length;
  centerLng = centerLng / polyCoords.length;

  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 10, //try something like (rightlat-leftlat) + (toplat-bottomlat) all * some constant to make it reasonable scale
    // zoom: 20 - (Math.round(latMax-latMin + lngMax-lngMin) % 19),// / (centerLat + centerLng);
    // zoom: 800 / (Math.max(latMax-centerLat, centerLat-latMin)**2 + Math.max(lngMax-centerLng, centerLng-lngMin)**2)**0.5,
    center: { lat: centerLat, lng: centerLng },
    mapTypeId: "satellite",
    gestureHandling: "greedy",
  });
  var sampleCoords = JSON.parse(document.getElementById('sampled_points').innerHTML);
  var fillOp = 0.35;

  if (sampleCoords.length > 0) {
    fillOp = 0.25;
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

  document.getElementById("api_failure").innerHTML = "";
}
