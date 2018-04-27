import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/here', methods=['POST'])
def here_is_shoebox():
    data = json.loads(request.data)
    lon,lat = data["lon"],data["lat"]
    try:
        return True
    except:
        return False

@app.route('/where', methods=['GET'])
def where_is_shoebox():
    data = json.loads(request.data)
    lon,lat = data["lon"],data["lat"]
    location = {"lon": 12,"lat": 34}
    return jsonify(location)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
