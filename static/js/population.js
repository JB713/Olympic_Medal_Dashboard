d3.json("/api/v1.0/countries_medals_count_population").then(
    populationData => {
        
        // svg params
        const svgHeight = 300;
        const svgWidth = 600;
        
        // margins
        const margin = {
            top: 50,
            right: 50,
            bottom: 50,
            left: 50
        };
        
        // chart area minus margins
        const chartHeight = svgHeight - margin.top - margin.bottom;
        const chartWidth = svgWidth - margin.left - margin.right;
        
        // create svg container
        const svg = d3.select("#populationmedals").append("svg")
            .attr("height", svgHeight)
            .attr("width", svgWidth);
        
        // shift everything over by the margins
        const chartGroup = svg.append("g")
            .attr("transform", `translate(${margin.left}, ${margin.top})`);
        
        let dataArray = populationData.map(data => data.medals_by_population);
        dataArray = dataArray.slice(0, 9);
        // scale y to chart height
        const yScale = d3.scaleLinear()
            .domain([0, d3.max(dataArray)])
            .range([chartHeight, 0]);
        
        let dataCategories = populationData.map(data => data.Country);
        dataCategories = dataCategories.slice(0, 9);
        const xScale = d3.scaleBand()
            .domain(dataCategories)
            .range([0, chartWidth])
            .padding(0.1);
        
        // create axes
        const yAxis = d3.axisLeft(yScale);
        const xAxis = d3.axisBottom(xScale);
        
        // set x to the bottom of the chart
        chartGroup.append("g")
            .attr("transform", `translate(0, ${chartHeight})`)
            .call(xAxis);
        
        // set y to the y axis
        chartGroup.append("g")
            .call(yAxis);
        
        
        chartGroup.selectAll("rect")
            .data(dataArray)
            .enter()
            .append("rect")
            .attr("x", (d, i) => xScale(dataCategories[i]))
            .attr("y", d => yScale(d))
            .attr("width", xScale.bandwidth())
            .attr("height", d => chartHeight - yScale(d))
            .attr("fill", "green")
            // event listener for onclick event
            .on("click", function (d, i) {
                alert(`${dataArray[i]}!`);
            })
            // event listener for mouseover
            .on("mouseover", function () {
                d3.select(this)
                    .attr("fill", "red");
            })
            // event listener for mouseout
            .on("mouseout", function () {
                d3.select(this)
                    .attr("fill", "green");
            });
        
    }
).catch(function (error) {
        console.log(error);
    }
);