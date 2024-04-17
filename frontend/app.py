from flask import Flask, render_template, request
from azure.storage.blob import BlobServiceClient, BlobClient
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DEBUG = logger.debug
INFO = logger.info
WARNING = logger.warning
ERROR = logger.error

load_dotenv()  # take environment variables from .env

app = Flask(__name__)

# Replace with your Azure Storage connection string

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

@app.route('/')
def index():
    DEBUG('Index route')
    return render_template('upload.html')

@app.route('/list')
def list_files():
    DEBUG('List route')
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blobs_list = container_client.list_blobs()
    return render_template('list.html', blobs=blobs_list)

@app.route('/upload', methods=['POST'])
def upload_file():
    DEBUG(upload_file)
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        # Create a blob client using the local file name as the name for the blob
        blob_client = BlobServiceClient.from_connection_string(connection_string).get_blob_client(container=container_name, blob=file.filename)

        # Check if the filename is already in use
        if blob_client.exists():
            INFO('Filename already in use')
            # If the filename is already in use, create a new filename
            file.filename = 'new_' + file.filename

        # Upload the created file
        blob_client.upload_blob(file)
        

        return 'File successfully uploaded'

if __name__ == '__main__':
    app.run(debug=True)
