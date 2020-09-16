console.log("World Map by Gender");

const worldMapByGender = L.map(
    "map_by_gender",
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
).addTo(worldMapByGender);

d3.json('/api/v1.0/medal_count_total_by_country').then(
    (medals_by_country) => {
        d3.json('/api/v1.0/medal_dict_gender').then(medal_dict_gender => {
            medals_by_country.forEach(countryData => {
                let countryMedalsByGender = medal_dict_gender[countryData.Code];
                
                if (!countryMedalsByGender) return;

                let popupContent = "<h1>" + countryData.Country + "</h1> <hr> <h3>Total medals: " + countryData.medals_count + "</h3>";
        
                let maleMedalCount = 0,
                  femaleMedalCount = 0;

                countryMedalsByGender.Year.forEach(
                    (year, index) => {
                        maleMedalCount += countryMedalsByGender.Male_Medal[index];
                        femaleMedalCount += countryMedalsByGender.Female_Medal[index];
                    }
                );
                popupContent += '<p>Male medals:' + maleMedalCount + '</p>';
                popupContent += '<p>Female medals:' + femaleMedalCount + '</p>';

                L.circle([countryData.latitude, countryData.longitude], {
                    color: 'red',
                    fillColor: '#f03',
                    fillOpacity: 0.5,
                    radius: 3000 + 100 * countryData.medals_count
                }).bindPopup(popupContent).addTo(worldMapByGender);

                // L.marker([countryData.latitude, countryData.longitude])
                //     .bindPopup(popupContent)
                //     .addTo(worldMapByGender);
                    
                });
            }
        );
    }
);