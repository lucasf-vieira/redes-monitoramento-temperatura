from flask import Flask, render_template, request, jsonify
import json


app = Flask(__name__)
data_file = 'data.json'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_data", methods=["GET"])
def get_data():
    try:
        with open(data_file, "r") as file:
            file_data = json.load(file)
    except FileNotFoundError:
        file_data = {
            "udp": "-1",
            "tcp": "-1",
            "mqtt": "-1"
        }

    return jsonify(file_data)


@app.route("/update_data", methods=["POST"])
def update_data():
    request_data = request.json
    try:
        with open(data_file, "r") as file:
            file_data = json.load(file)
    except FileNotFoundError:
        file_data = {}

    for key in request_data:
        file_data[key] = request_data[key]

    with open(data_file, "w") as file:
        json.dump(file_data, file)

    return "Data received successfully"


if __name__ == "__main__":
    app.template_folder = "templates"
    app.run(host="0.0.0.0")
