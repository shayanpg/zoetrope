// This example creates a simple polygon representing the Bermuda Triangle.

// function initMap() {
//
//
//   // This is probably a sloppy way to do this?  The neighborhood definition gets taken from the model and stored
//   //in a hidden attribute in HTML
//   var polyCoords = JSON.parse(document.getElementById('neighborhood_def').innerHTML)
//   var centerPoint = JSON.parse(document.getElementById('neighborhood_center').innerHTML)
//
//   var map = new google.maps.Map(document.getElementById('map'), {
//     zoom: 15,
//     // center: centerPoint,
//     center: { lat: -34.397, lng: 150.644 },
//     mapTypeId: 'terrain'
//   });
//
//   // Construct the polygon.
//   var neighborhood = new google.maps.Polygon({
//     paths: polyCoords,
//     strokeColor: '#FF0000',
//     strokeOpacity: 0.8,
//     strokeWeight: 2,
//     fillColor: '#FF0000',
//     fillOpacity: 0.35
//   });
//
//   neighborhood.setMap(map);
// }

//TODO Remove all this down to line 40
// let map;
//
// function initMap() {
//   map = new google.maps.Map(document.getElementById("map"), {
//     center: { lat: -34.397, lng: 150.644 },
//     zoom: 8,
//   });
// }

// This example creates a simple polygon representing the Bermuda Triangle.
function initMap() {
  var polyCoords = JSON.parse(document.getElementById('neighborhood_def').innerHTML)
  // document.getElementById('test').innerHTML = document.getElementById('neighborhood_def').innerHTML

  var centerLat = 0;
  for (let i = 0; i < polyCoords.length; i++) centerLat += polyCoords[i]["lat"];
  centerLat = centerLat / polyCoords.length;

  var centerLng = 0;
  for (let i = 0; i < polyCoords.length; i++) centerLng += polyCoords[i]["lng"];
  centerLng = centerLng / polyCoords.length;

  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    // center: { lat: 38.578150, lng: -121.485202 },
    center: { lat: centerLat, lng: centerLng },
    mapTypeId: "terrain",
  });
  // Define the LatLng coordinates for the polygon's path.
  const triangleCoords = [
    { lat: 38.578150, lng: -121.485202 },
    { lat: 38.575276, lng: -121.474581 },
    { lat: 38.580765, lng: -121.4722 }
  ];
  // Construct the polygon.
  const bermudaTriangle = new google.maps.Polygon({
    // paths: triangleCoords,
    paths: polyCoords,
    strokeColor: "#FF0000",
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: "#FF0000",
    fillOpacity: 0.35,
  });

  bermudaTriangle.setMap(map);
}

function randomBetween(min, max) {
    return min + (Math.random() * diff(min, max));
}


function sample(polyCoordsString, centerPointString, numSamplePoints) {

  //right now, the neighborhood definition is an argument.  In initMap() we pull it out of HTML....the argument approach
  //may be useful in the future?

  //define the area within which to sample
  var polyCoords = JSON.parse(polyCoordsString);
  var centerPoint = JSON.parse(centerPointString)

  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 17,
    center: centerPoint,
    mapTypeId: 'terrain'
  });


  // Construct the polygon.
  var neighborhood = new google.maps.Polygon({
    paths: polyCoords,
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: '#FF0000',
    fillOpacity: 0.35
  });

  neighborhood.setMap(map);

  furthestDist = getFurthestDist(polyCoords, centerPoint);


  var sampled_points = [];
  var i=0;
   while (i < numSamplePoints) {

        //the way we're doing this right now is kinda dumb...draw a big box around the neighborhood and sample randomly within that box
        var point_lat = randomBetween((centerPoint["lat"] - furthestDist), (centerPoint["lat"] + furthestDist));
        var point_lng = randomBetween((centerPoint["lng"] - furthestDist), (centerPoint["lng"] + furthestDist));

        var point_location = new google.maps.LatLng(point_lat, point_lng);


        if (google.maps.geometry.poly.containsLocation(point_location, neighborhood)) {
        //if (true) {
            new google.maps.Marker({
                position: point_location,
                map: map,
                icon: {
                  path: google.maps.SymbolPath.CIRCLE,
                  fillColor: 'blue',
                  fillOpacity: .9,
                  strokeColor: 'black',
                  strokeWeight: .9,
                  scale: 3
                }
            });

            sampled_points.push(point_location);
            i++;
        }
// >>>>>>> 08a059da2c38366675638d0f34452dde27ea29c8
   }

    return sampled_points
}

function diff(a,b){return Math.abs(a-b);}

function getFurthestDist(polygonPointArray, centerPoint) {
    //returns the farthest max lat/lng of the polygon, so that we can sample in a rectangle which contains the entire neighborhood
    //This is a pretty inelegant way to do this and will result in picking many points outside the actual polygon, but whatever for now

    var numBorderPoints = polygonPointArray.length
    var maxDist = 0

    for (var i = 0; i< numBorderPoints; i++) {
        latDist = Math.abs(polygonPointArray[i]["lat"] - centerPoint["lat"])
        lngDist = Math.abs(polygonPointArray[i]["lng"] - centerPoint["lng"])
        if ( latDist > maxDist) {
            maxDist = latDist;
        }
        if ( lngDist > maxDist) {
            maxDist = lngDist;
        }
    }

    return maxDist;

}

function download_imgs() {
  var xhttp = new XMLHttpRequest();

  var url = "index"
  var url_plus_payload = url + "?points=" + document.getElementById("sampled_points_input").innerHTML

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     document.getElementById("sampled_points_input").innerHTML = this.responseText;
    }
  };
  xhttp.open("POST", url_plus_payload, true);
  xhttp.send();
}
