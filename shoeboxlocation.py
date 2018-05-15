# -*- coding: utf-8 -*-
"""API for retrieving updating and retrieving the location of an indoor object (shoebox).

This Flask application is build as a Proof of Concept at Tensing. It is part of
an Indoor Wayfinding application, where an asset can be tracked in the office
space using bluetooth beacons. The application contains 2 endpoints, one where
the assets sends its updated location information. The other endpoint is for
requesting the latest known location of the asset.
"""

import os
import json
import datetime
import dropbox
from flask import Flask, request, jsonify

# Retrieve global variables
filelocation = os.path.dirname(os.path.abspath(__file__))
configfile = os.path.join(filelocation,'config.cfg')
app = Flask(__name__)
if "FILE" in os.environ and "TOKEN" in os.environ:
    # Use Heroku environment variables
    filename = os.getenv("FILE")
    access_token = os.getenv("TOKEN")
elif os.path.isfile(configfile):
    # Use config file for testing locally
    app.config.from_pyfile('config.cfg')
    filename = app.config["FILE"]
    access_token = app.config["TOKEN"]
else:
    raise ValueError('No file or token found..')

# Initialize dropbox session
dbx = dropbox.Dropbox(access_token)
mode = dropbox.files.WriteMode.overwrite

# Endpoints
@app.route('/here', methods=['POST'])
def here_is_shoebox():
    """Endpoint for updating the shoebox location. It accepts POST requests with
    a JSON string containing "lat" and "lon" values (latitude and longitude
    coordinates in WGS84)."""
    # Check if data can be read
    data = request.data
    try:
        data = data.decode()
    except AttributeError:
        return "Could not read post body", 400
    # Check if data contains JSON object
    try:
        data = json.loads(data)
    except:
        return "Please provide a JSON string", 400
    # Check if lat and lon are present and of type float
    if not "lat" in data.keys() or not "lon" in data.keys():
        return "Please provide 'lat' and 'lon' coordinates in the post body.", 400
    elif not isinstance(data['lat'], float) or not isinstance(data['lon'], float):
        return "Please provide 'lat' and 'lon' coordinates as type float.", 400
    # If data is correct, write it to file
    res = dbx.files_upload(json.dumps(data).encode(), filename, mode,
        client_modified=datetime.datetime.now(),
        mute=True)
    return "success"

@app.route('/where', methods=['GET'])
def where_is_shoebox():
    """Endpoint for retrieving the shoebox location. It returns a JSON string
    containing "lat" and "lon" values (latitude and longitude coordinates in
    WGS84)."""
    metadata,res = dbx.files_download(filename)
    location = json.loads(res.content)
    return jsonify(location)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
