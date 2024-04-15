from flask import Flask, render_template, request
from azure.storage.blob import BlobServiceClient, BlobClient
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

app = Flask(__name__)

# Replace with your Azure Storage connection string

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        # Create a blob client using the local file name as the name for the blob
        blob_client = BlobServiceClient.from_connection_string(connection_string).get_blob_client(container=container_name, blob=file.filename)

        # Upload the created file
        blob_client.upload_blob(file)

        return 'File successfully uploaded'

if __name__ == '__main__':
    app.run(debug=True)
