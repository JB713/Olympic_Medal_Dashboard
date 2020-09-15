from Services import Services
from flask import Flask, jsonify, render_template

app = Flask(__name__)

data = Services()


@app.route('/')
@app.route('/home')
@app.route('/index')
@app.route('/index.html')
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


@app.route("/api/v1.0/countries_medals_count_population")
def get_countries_medals_count_population():
    return jsonify(data.get_countries_medals_count_population())


@app.route("/api/v1.0/medal_dict_gender")
def gender_medal_dict():
    return jsonify(data.gender_medal_dict())


@app.route("/api/v1.0/country_codes")
def get_country_codes():
    return jsonify(data.get_country_codes())


# Retrieve medal count total by country and year
@app.route('/api/v1.0/medal_count_by_country_and_year')
def get_medal_count_by_country_and_year():
    return jsonify(data.get_medal_count_by_country_and_year())


# Retrieve medal count total for all countries
@app.route('/api/v1.0/medal_count_total_by_country')
def get_medal_count_total_by_country():
    return jsonify(data.get_medal_count_total_by_country())


# Retrieve medal counts by type of medal for a country
@app.route('/api/v1.0/get_country_medals/<country_name>')
def get_country_medals(country_name):
    return jsonify(data.get_country_medals(country_name))


if __name__ == "__main__":
    app.run(debug=True)
