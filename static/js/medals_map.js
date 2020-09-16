console.log("World Map");

const worldMap = L.map(
    "map",
    {
        center: [26, -95],
        zoom: 4
    }
);

L.tileLayer(
    "https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
    {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        id: "light-v10",
        accessToken: API_KEY
    }
).addTo(worldMap);


const GOLD_COLOR = "#FFD700";
const SILVER_COLOR = "#c0c0c0";
const BRONZE_COLOR = "#CD7F32";

const colors = {
    "Gold": GOLD_COLOR,
    "Silver": SILVER_COLOR,
    "Bronze": BRONZE_COLOR
}

d3.json('/api/v1.0/medal_count_total_by_country').then(
    (medals_by_country) => {
        medals_by_country.forEach(
            countryData => {
                d3.json(
                    '/api/v1.0/get_country_medals/' + countryData.Country
                ).then(
                    countryMedals => {
                        let popupContent = "<h1>" + countryData.Country + "</h1> <hr> <h3>Total medals: " + countryData.medals_count + "</h3>";
                        
                        countryMedals.forEach(
                            medal => {
                                //console.log(colors[medal.Medal])
                                popupContent += '<i style="background:' + colors[medal.Medal] + '"></i> ' + medal.medals_count + '<br>';
                                
                            }
                        );
                        
                        L.marker([countryData.latitude, countryData.longitude])
                            .bindPopup(popupContent)
                            .addTo(worldMap);
                    }
                );
            }
        );
    }
);