#!/usr/bin/env python
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

# Global variables
app = Flask(__name__)
filename = os.getenv("FILE")
access_token = os.getenv("TOKEN")
dbx = dropbox.Dropbox(access_token)
mode = dropbox.files.WriteMode.overwrite

# Endpoints
@app.route('/here', methods=['POST'])
def here_is_shoebox():\
    """Endpoint for updating the shoebox location. It accepts POST requests with
    a JSON string containing "lat" and "lon" values (latitude and longitude
    coordinates in WGS84)."""
    data = request.data
    res = dbx.files_upload(data, filename, mode,
        client_modified=datetime.datetime.now(),
        mute=True)
    return jsonify(data)

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
