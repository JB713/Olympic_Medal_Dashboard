console.log("START");
d3.json('/api/v1.0/medals').then(
    (medalsData) => {
        console.log("medals data: " + medalsData);

        var tbody = d3.select("tbody");
        
        medalsData.forEach(
            (medal) => {
                console.log("medal: " + medal);
                var row = tbody.append("tr");
                var cell_id = row.append("td");
                var cell_name = row.append("td");
                cell_id.text(medal.medal_id);
                cell_name.text(medal.Medal);
            }
        );
    }
);