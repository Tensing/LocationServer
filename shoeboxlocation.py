import json
import dropbox
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
filename = app.config["FILE"]
access_token = app.config["TOKEN"]
dbx = dropbox.Dropbox(access_token)
mode = dropbox.files.WriteMode.overwrite

@app.route('/here', methods=['POST'])
def here_is_shoebox():
    data = json.loads(request.data)
    res = dbx.files_upload(data, filename, mode,
        client_modified=datetime.datetime.now(),
        mute=True)

@app.route('/where', methods=['GET'])
def where_is_shoebox():
    metadata,res = dbx.files_download(filename)
    location = json.loads(res.content)
    return jsonify(location)

if __name__ == '__main__':
    app_setup()
    app.run(debug=True, threaded=True)
