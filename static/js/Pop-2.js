const svgWidth = 600;
const svgHeight = 300;

const margin = {
    top: 20,
    right: 40,
    bottom: 60,
    left: 100
};

const width = svgWidth - margin.left - margin.right;
const height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
const svg = d3.select("#populationmedals")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

const chartGroup = svg.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Import Data
d3.json("/api/v1.0/countries_medals_count_population").then(
    populationData => {
        
        let scatterData = populationData.map(
            data => {
                return {
                    medals : data.num_medals,
                    population : data.Population
                }
            }
        );
        
        scatterData = scatterData.slice(0, 19);
        const xLinearScale = d3.scaleLinear()
            .domain(
                [
                    d3.min(demoFactors, d => d.medals) * 0.95,
                    d3.max(scatterData, d => d.medals) * 1.04
                ]
            )
            .range([0, width]);
        
        const yLinearScale = d3.scaleLinear()
            .domain(
                [
                    d3.min(demoFactors, d => d.population) * 0.7,
                    d3.max(scatterData, d => d.population) * 1.07
                ]
            )
            .range([height, 0]);
        
        const bottomAxis = d3.axisBottom(xLinearScale);
        const leftAxis = d3.axisLeft(yLinearScale);
        
        chartGroup.append("g")
            .attr("transform", `translate(0, ${height})`)
            .call(bottomAxis);
        
        chartGroup.append("g")
            .call(leftAxis);
        
        // Step 5: Create Circles
        // ==============================
        const circlesGroup = chartGroup.selectAll("circle")
            .data(scatterData)
            .enter()
            .append("circle")
            .attr("cx", d => xLinearScale(d.medals))
            .attr("cy", d => yLinearScale(d.population))
            .attr("r", "15")
            .attr("fill", "pink")
            .attr("opacity", ".5");
        
        // // Step 6: Initialize tool tip
        // // ==============================
        // const toolTip = d3.tip()
        //     .attr("class", "tooltip")
        //     .offset([80, -60])
        //     .html(function (d) {
        //         return (`${d.rockband}<br>Hair length: ${d.hair_length}<br>Hits: ${d.num_hits}`);
        //     });
        //
        // // Step 7: Create tooltip in the chart
        // // ==============================
        // chartGroup.call(toolTip);
        
        // // Step 8: Create event listeners to display and hide the tooltip
        // // ==============================
        // circlesGroup.on("click", function (data) {
        //     toolTip.show(data, this);
        // })
        //     // onmouseout event
        //     .on("mouseout", function (data, index) {
        //         toolTip.hide(data);
        //     });
        
        // Create axes labels
        chartGroup.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 0 - margin.left + 40)
            .attr("x", 0 - (height / 2))
            .attr("dy", "1em")
            .attr("class", "axisText")
            .text("Number of Billboard 100 Hits");
        
        chartGroup.append("text")
            .attr("transform", `translate(${width / 2}, ${height + margin.top + 30})`)
            .attr("class", "axisText")
            .text("Hair Metal Band Hair Length (inches)");
    }).catch(function (error) {
    console.log(error);
});
