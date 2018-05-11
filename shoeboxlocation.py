import os
import json
import datetime
import dropbox
from flask import Flask, request, jsonify

app = Flask(__name__)
filename = os.getenv("FILE")
access_token = os.getenv("TOKEN")
dbx = dropbox.Dropbox(access_token)
mode = dropbox.files.WriteMode.overwrite

@app.route('/here', methods=['POST'])
def here_is_shoebox():
    data = request.data
    res = dbx.files_upload(data, filename, mode,
        client_modified=datetime.datetime.now(),
        mute=True)
    return "success"

@app.route('/where', methods=['GET'])
def where_is_shoebox():
    metadata,res = dbx.files_download(filename)
    location = json.loads(res.content)
    return jsonify(location)

if __name__ == '__main__':
    app_setup()
    app.run(debug=True, threaded=True)
