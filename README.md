# Olympic_Medal_Dashboard

## Objective
The objective of this study was to visualize countries' summer and winter olympic performance through the history of the modern olympic games.
The final dashboard link is at https://olympic-games-dashboard.herokuapp.com/

## Dataset
Data was gathered from kaggle https://www.kaggle.com/the-guardian/olympic-games.
It was mostly a clean dataset which consist of 3 csv files: 1) dictionary.csv has 4 columns as "Country", "Code", "Population" and "GDP per Capita" 
2) summer.csv has "Year", "City", "Sport", "Discipline", "Athlete", "Country", "Gender", "Event" and "Medal" for summer olympics.  3) winter.csv has exactly the same columns
with summer.csv for winter olympics.  

The dataset was loaded to Postgresql database and then deployed to Heroku.

## Analysis
As analysis, we have mainly focused on countries' medal distributions in different aspects.  
![Map1] (https://github.com/JB713/Olympic_Medal_Dashboard/blob/master/static/assets/Map1.PNG?raw=true)

Initially, a world map was plotted showing individual countries with total medals won so far in both summer and winter olympics and the distribution of gold, silver and bronze.

![BarChart1] (https://github.com/JB713/Olympic_Medal_Dashboard/blob/master/static/assets/BarChart1.PNG?raw=true)

Then, the dataset from 1994 to 2014 was sliced to understand the distribution of male vs. female medal winners per country.

![BarChart2] (https://github.com/JB713/Olympic_Medal_Dashboard/blob/master/static/assets/BarChart2.PNG?raw=true)

Finally, it was analyzed how many people does it take to win one medal relative to total population.

## Technology 
For this dashboard, for data cleanup, wranglig, slicing and ETL, python libraries pandas and numpy were heavily used.  The database was deployed to Postgresql, a relational database in second normal form was created.  For the necessary api routes, Flask with python was used. HTML, CSS and JavaScript (more specifiallyBootstrap, plotly.js, leaflet.js and d3.js) were used for the frontend of the dashboard.  The entire application was deployed on Heroku.

