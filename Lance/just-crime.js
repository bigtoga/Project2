var myMap = L.map("map", {
  center: [37.7749, -122.4194],
  zoom: 13
});

// Adding tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);

var url = "https://data.sfgov.org/resource/wg3w-h783.json?$limit=500";

d3.json(url, function (data) {
  console.log(data);
  data.forEach(data => {
    data.longitude = +data.longitude;
    data.latitude = +data.latitude
  });

  function checkPoints(cat) {
    return cat === "Offences Against The Family And Children" ? "blue" :
        cat === "Assault" ? "green" :
            cat === "Burglary" ? "orange" :
                cat === "Robbery" ? "purple" :
                    cat === "Homicide" ? "red" :
                        "lightgray";
}


  for (var i = 0; i < data.length; i++) {
    var locLat = data[i].latitude;
    var locLon = data[i].longitude;
    var point = data[i].point;
    // console.log(locLat)
    // console.log(locLon)
    // console.log(latitude)
    console.log(data[i].incident_category)
    if (point) {
      L.circle([locLat, locLon], {
        fillOpacity: .8,
        color: checkPoints(data[i].incident_category),
        fillColor: checkPoints(data[i].incident_category),
        radius: 100
      })
        .bindPopup("<h2> Incident Category : " + data[i].incident_category +
          "</h2><hr><h3>" + data[i].incident_subcategory +
          "</h3><hr><p>" + data[i].incident_description + "</p>").addTo(myMap);
    }
  }
});

