
  function xyData(country_code, dictionary, yDataType) {
    // Define a variable for the data array for the specified country
    var country_data = dictionary[country_code];
    // console.log('country_data',country_data)
   
    var x = country_data.Year;

    //Define conditional to set the y data array based on the yDataType argument
    if (yDataType == 'Female_Medal') {
        var y = country_data.Female_Medal;
    }
    else if (yDataType == 'Year') {
        var y = country_data.Year;
    }
    else if (yDataType == 'Male_Medal') {
      var y = country_data.Male_Medal;
    };

    
    return [x, y];
};
  

  function barGraph(country) {
    
    // Grab the json from that url and utilize it to build the line graph
    d3.json("/api/v1.0/medal_dict_gender").then(function(response) {


        // console.log(response);
        
        // Define trace for the population line graph with AUT as the placeholder
        var male_trace = {
            x: xyData(country_code=country, dictionary=response, yDataType='Male_Medal')[0],
            y: xyData(country_code=country, dictionary=response, yDataType='Male_Medal')[1],
            type: 'bar',
            name: 'Male',
            marker:{color: 'rgb(107 150 255)'}
            
        };

        var female_trace = {
          x: xyData(country_code=country, dictionary=response, yDataType='Female_Medal')[0],
          y: xyData(country_code=country, dictionary=response, yDataType='Female_Medal')[1],
          type: 'bar',
          name: 'Female',
          marker:{color: 'rgb(177, 10, 236)'}
          
      };
      
                
        var data = [male_trace, female_trace];
        
        
          var layout = {
            title: 'Female vs. Male Medal Winners',
            xaxis: {
              tickmode: "array",
              tickvals: [1994, 1996, 1998, 2000, 2002, 2004,2006,2008,2010,2012,2014],
              tickvals: [1994, 1996, 1998, 2000, 2002, 2004,2006,2008,2010,2012,2014],
              //autotick: false,
              title: "Years",
              titlefont:{
                size:16
              },
              tickfont: {
                size: 14,
                color: 'rgb(107, 107, 107)'
              }},
            yaxis: {
              title: 'Total Medal',
              titlefont: {
                size: 16,
                color: 'rgb(107, 107, 107)'
              },
              tickfont: {
                size: 14,
                color: 'rgb(107, 107, 107)'
              }
            },
            legend: {
              x: 0,
              y: 1.0,
              bgcolor: 'rgba(255, 255, 255, 0)',
              bordercolor: 'rgba(255, 255, 255, 0)'
            },
            barmode: 'group',
            bargap: 0.15,
            bargroupgap: 0.1
          };
        
        Plotly.newPlot('bar', data, layout);
        
        
    });
};

  function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selCountrySet");

  // Use the list of sample names to populate the select options
  d3.json('api/v1.0/country_codes').then(function(response) {

    let country_codes = response
    country_codes.forEach(
      (country_code) => {
          selector.append("option")
                  .text(country_code)
                  .property("value", country_code);
        }
    )
    //
    const firstCountry = country_codes[0];
    barGraph(firstCountry);
    
  });
  }


function optionChanged(newCountry) {
  barGraph(newCountry);
};

// Call the init() function
init();
      //}

