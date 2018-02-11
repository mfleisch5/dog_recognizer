import os
from flask import Flask, redirect, url_for, json
from flask import request
from werkzeug.utils import secure_filename

import sys
sys.path.insert(0, "/home/ubuntu/dog_recognizer")
import api_mgr
import base64

application = Flask(__name__)

UPLOAD_FOLDER = '/var/www/uploads/'
ALLOWED_EXTENSIONS = (['png','jpg','jpeg','gif'])
application.config['UPLOAD FOLDER'] = UPLOAD_FOLDER
application.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/')
def index():
    return 'Hello dogs'

@application.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return json.dumps("")
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        #if file.size <= 0:
        #    return json.dumps("")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            thepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(thepath)
            return json.dumps([api_mgr.predict(thepath)])

    return json.dumps("");

application.debug = True

if __name__ == '__main__':
    application.run()

