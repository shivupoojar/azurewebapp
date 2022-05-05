import json
import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from azure.storage.blob.aio import BlobClient
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__,
            static_url_path='/raw',
            static_folder='raw')

account_access_key = 'g97DXk+n5KfKTj7hQgDCghwRk4aZSvYJwu2D87vfgp/6AfRm5uUtBQUR8uhMIT/5t8dfHin/nUbp30KdSKcCJg=='
account_url = "https://poojaralab14.blob.core.windows.net/"
connection_string = "DefaultEndpointsProtocol=https;AccountName=%s;AccountKey=%s;EndpointSuffix=core.windows.net" %\
                    ("poojaralab14", account_access_key)
blob_client = BlobServiceClient(account_url="https://poojaralab14.blob.core.windows.net/",
                                credential=account_access_key)

UPLOAD_FOLDER = 'raw'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def read_messages_from_file():
    """ Read all messages from a JSON file"""
    with open('data.json') as messages_file:
        return json.load(messages_file)


def store_message(content, img_path):
    """ Read the contents of JSON file, add this message to it's contents, then write it back to disk. """
    data = read_messages_from_file()
    new_message = {
        'content': content,
        'image_path': img_path,
        'timestamp': datetime.now().isoformat(" ", "seconds")
    }
    data['messages'].append(new_message)
    with open('data.json', mode='w') as messages_file:
        json.dump(data, messages_file)


def insert_blob_data(image):
    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name="raw", blob_name="rawdata")

    with open(image, "rb") as data:
        uploaded = blob.upload_blob(data)
        print(str(uploaded))


# The Flask route, defining the main behaviour of the webserver:
@app.route("/", methods = ['GET', 'POST'])
def home():
    new_message = request.form.get('msg')
    data = read_messages_from_file()
    if 'image' not in request.files:
        return render_template('home.html', messages=data['messages'])

    # Handle Image:
    image_file = request.files['image']

    if new_message and image_file:
        if allowed_file(image_file.filename):
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename))
            image_file.save(img_path)
            # insert_blob_data(image_file) #TODO
            store_message(new_message, img_path)

    # Return a Jinja HTML template, passing the messages as an argument to the template:
    return render_template('home.html', messages=data['messages'])

if __name__ == '__main__':
    app.run()