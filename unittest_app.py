import json
import dropbox
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
filename = app.config["FILE"]
access_token = app.config["TOKEN"]
dbx = dropbox.Dropbox(access_token)
mode = dropbox.files.WriteMode.overwrite

@app.route('/here', methods=['POST'])
def here_is_shoebox():
    data = request.data
    res = dbx.files_upload(data, filename, mode,
        client_modified=datetime.datetime.now(),
        mute=True)
    return ""

@app.route('/where', methods=['GET'])
def where_is_shoebox():
    try:
        md, res = dbx.files_download(filename)
    except dropbox.exceptions.HttpError as err:
        print('*** HTTP error', err)
        return None

    location = json.loads(res.content)
    return jsonify(location)



# import shoeboxlocation
import unittest
test_json = '{"lon": 12,"lat": 41}'

class TestIntegrations(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_post(self):
        res = self.app.post('/here', json=test_json)
        self.assertEqual(res.status_code, 200)

    def test_get(self):
        res = self.app.get('/where')
        s = res.data
        result = json.loads(s)
        print(type(result))
        print(result)
        # self.assertEqual(result, json.loads(test_json))

if __name__ == '__main__':
    unittest.main()
