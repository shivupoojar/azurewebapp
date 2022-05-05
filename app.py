import json
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from azure.storage.blob.aio import BlobClient
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

account_access_key = 'g97DXk+n5KfKTj7hQgDCghwRk4aZSvYJwu2D87vfgp/6AfRm5uUtBQUR8uhMIT/5t8dfHin/nUbp30KdSKcCJg=='
azure_service = BlobServiceClient(account_url="https://poojaralab14.blob.core.windows.net/", credential=account_access_key)
app = Flask(__name__)

UPLOAD_FOLDER = 'raw'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_messages_from_file():
    """ Read all messages from a JSON file"""
    with open('data.json') as messages_file:
        return json.load(messages_file)


def append_message_to_file(content):
    """ Read the contents of JSON file, add this message to it's contents, then write it back to disk. """
    data = read_messages_from_file()
    new_message = {
        'content': content,
        'timestamp': datetime.now().isoformat(" ", "seconds")
    }
    data['messages'].append(new_message)
    with open('data.json', mode='w') as messages_file:
        json.dump(data, messages_file)

def insert_blob_data(image):
    blob = BlobClient.from_connection_string(conn_str=azure_service, container_name="raw", blob_name="rawdata")
    with open(image, "rb") as data:
        blob.upload_blob(data)

# The Flask route, defining the main behaviour of the webserver:
@app.route("/")
def home():
    new_message = request.args.get('msg')
    data = read_messages_from_file()
    if 'file' not in request.files:
        return render_template('home.html', messages=data['messages'])
    file = request.files['file1']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        insert_blob_data(file)

    if new_message:
        append_message_to_file(new_message)

   

    # Return a Jinja HTML template, passing the messages as an argument to the template:
    return render_template('home.html', messages=data['messages'])
