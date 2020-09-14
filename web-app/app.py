
from Services import Services
from flask import Flask, jsonify, render_template

# create instance of Flask app
app = Flask(__name__)

data = Services()


@app.route('/index.html', methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/api/v1.0/medals")
def get_all_medals():
    return jsonify(data.get_medals())


@app.route("/api/v1.0/country/<country_name>")
def get_country_info_by_name(country_name):
    return jsonify(data.get_country_info_by_name(country_name))


@app.route("/api/v1.0/countries")
def get_countries():
    return jsonify(data.get_countries())


# Retrieve all medals and athletes
@app.route("/api/v1.0/countries_medals")
def get_countries_medals_count():
    return jsonify(data.get_countries_medals_count())

# My Gender app route
@app.route("/api/v1.0/gender_medals")
def get_gender_medals_count():
    return jsonify(data.get_gender_medals_count())

@app.route("/api/v1.0/countries_medals_count_population")
def get_gender_medals_count():
    return jsonify(data.countries_medals_count_population())



if __name__ == "__main__":
    app.run(debug=True)
