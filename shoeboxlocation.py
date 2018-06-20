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
import geojson
import datetime
import dropbox
from flask import Flask, request, jsonify

# Retrieve global variables
filelocation = os.path.dirname(os.path.abspath(__file__))
configfile = os.path.join(filelocation,'config.cfg')
app = Flask(__name__)
if "FILE" in os.environ and "TOKEN" in os.environ:
	# Use Heroku environment variables
	print("a")
	filename = os.getenv("FILE")
	filename_bot = os.getenv("FILE_BOT")
	access_token = os.getenv("TOKEN")
elif os.path.isfile(configfile):
	print("b")
	# Use config file for testing locally
	app.config.from_pyfile('config.cfg')
	filename = app.config["FILE"]
	filename_bot = app.config["FILE_BOT"]
	access_token = app.config["TOKEN"]
else:
	print("c")
	raise ValueError('No file or token found..')

# Initialize dropbox session
dbx = dropbox.Dropbox(access_token)
mode = dropbox.files.WriteMode.overwrite

# Endpoints
@app.route('/here', methods=['POST'])
def here_is_shoebox():
	"""Endpoint for updating the shoebox location. It accepts POST requests with
	a GeoJSON string containing a single point feature."""
	# Check if data can be read
	data = request.data
	try:
		data = data.decode()
	except AttributeError:
		return "Could not read post body", 400
	# Check if data contains a valid GeoJSON object
	try:
		data = geojson.loads(data)
	except:
		return "Please provide a GeoJSON string", 400
	# Check if only data contains a single point feature
	if not data.type.lower() == "feature" or not data.geometry.type.lower() == "point":
		return "Please provide a single GeoJSON point feature", 400
	# If data is correct, write it to file
	res = dbx.files_upload(json.dumps(data).encode(), filename, mode,
		client_modified=datetime.datetime.now(),
		mute=True)
	return "Location update successful"

@app.route('/where', methods=['GET'])
def where_is_shoebox():
	"""Endpoint for retrieving the shoebox location. It returns a GeoJSON string
	containing a single point feature with the last known location of the shoebox."""
	metadata,res = dbx.files_download(filename)
	location = json.loads(res.content)
	return jsonify(location)

@app.route('/here_robot', methods=['POST'])
def here_is_robot():
	"""Endpoint for updating the robot location. It accepts POST requests with
	a GeoJSON string containing a single point feature."""
	# Check if data can be read
	data = request.data
	try:
		data = data.decode()
	except AttributeError:
		return "Could not read post body", 400
	# Check if data contains a valid GeoJSON object
	try:
		data = geojson.loads(data)
	except:
		return "Please provide a GeoJSON string", 400
	# Check if only data contains a single point feature
	if not data.type.lower() == "feature" or not data.geometry.type.lower() == "point":
		return "Please provide a single GeoJSON point feature", 400
	# If data is correct, write it to file
	res = dbx.files_upload(json.dumps(data).encode(), filename_bot, mode,
		client_modified=datetime.datetime.now(),
		mute=True)
	return "Location update successful"

@app.route('/where_robot', methods=['GET'])
def where_is_robot():
	"""Endpoint for retrieving the robot location. It returns a GeoJSON string
	containing a single point feature with the last known location of the shoebox."""
	metadata,res = dbx.files_download(filename_bot)
	location = json.loads(res.content)
	return jsonify(location)
	
if __name__ == '__main__':
	app.run(debug=False, threaded=True)
