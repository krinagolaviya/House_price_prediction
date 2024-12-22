function getBathValue() {
  var uiBathrooms = document.getElementsByName("uiBathrooms");
  for (var i in uiBathrooms) {
    if (uiBathrooms[i].checked) {
      return parseInt(i) + 1;
    }
  }
  return -1; // Invalid Value
}

function getBHKValue() {
  var uiBHK = document.getElementsByName("uiBHK");
  for (var i in uiBHK) {
    if (uiBHK[i].checked) {
      return parseInt(i) + 1;
    }
  }
  return -1; // Invalid Value
}

function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");
  var sqft = document.getElementById("uiSqft");
  var bhk = getBHKValue();
  var bathrooms = getBathValue();
  var location = document.getElementById("uiLocations");
  var estPrice = document.getElementById("uiEstimatedPrice");
  var recommand = document.getElementById("recommand");

  var url = "http://127.0.0.1:5000/predict_home_price"; //Use this if you are NOT using nginx which is first 7 tutorials
  // var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards

  $.post(
    url,
    {
      total_sqft: parseFloat(sqft.value),
      bhk: bhk,
      bath: bathrooms,
      location: location.value,
    },
    function (data, status) {
      console.log(data.estimated_price);
      estPrice.innerHTML =
        "<h2>" +
        data.estimated_price.toString() +
        " </h2><br>" +
        data.extra.toString();
      console.log(status);
    }
  );

  var url2 = "http://127.0.0.1:5000/get_graph_data";
  $.post(
    url2,
    {
      bhk: bhk,
    },
    function (graphJSON, status) {
      console.log("got response for get_graph_data request");
      // console.log(location.value);
      if (graphJSON) {
        Plotly.newPlot(
          "graph",
          JSON.parse(graphJSON).data,
          JSON.parse(graphJSON).layout
        );
      }
    }
  );

  var url3 = "http://127.0.0.1:5000/get_recommand_data";
  $.post(
    url3,
    {
      location: location.value
    },
    function (data, status) {
      console.log("got response for get_recommand_data request");
      var list = "";
      for(entry of data){
        list += "<li>"+ entry+"</li>";
      }
      recommand.innerHTML ="<div class=\"innerdiv\"><div> <h2 style=\"text-align: center\">Recommanded Area</h2></div> <ul class=\"ulist \">" +  list + "</ul></div>";
    }
  );
}

function onPageLoad() {
  console.log("document loaded");
  var url = "http://127.0.0.1:5000/get_location_names"; // Use this if you are NOT using nginx which is first 7 tutorials
  // var url = "/api/get_location_names"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
  $.get(url, function (data, status) {
    console.log("got response for get_location_names request");
    if (data) {
      var locations = data.location;
      var uiLocations = document.getElementById("uiLocations");
      $("#uiLocations").empty();
      for (var i in locations) {
        var opt = new Option(locations[i]);
        $("#uiLocations").append(opt);
      }
    }
  });
}

window.onload = onPageLoad;
