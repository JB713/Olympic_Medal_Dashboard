
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


if __name__ == "__main__":
    app.run(debug=True)
