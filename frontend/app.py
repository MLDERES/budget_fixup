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

# Load the Excel file
def parse_work_tags_column(file_path):
    df = pd.read_excel(file_path)

    # This function will parse the 'work tags' column into separate columns
    #  it's called as a vector operation on the 'work tags' column
    def parse_work_tags(work_tags):
        tag_dict = {}
        lines = work_tags.split('\n')
        for line in lines:
            if line.strip():  # Skip empty lines
                tag_name, tag_value = line.strip().split(': ')
                tag_dict[tag_name] = tag_value
        return tag_dict

    # Apply the parse_work_tags function to the 'work tags' column and expand it into separate columns
    df_worktags = df['Worktags'].apply(parse_work_tags).apply(pd.Series)

    # Concatenate the original DataFrame with the parsed work tags columns
    result_df = pd.concat([df, df_worktags], axis=1)

    # Drop the original 'work tags' column if needed
    columns_to_drop = ['Worktags','Accounting Date', 'Operational Transaction', 'Journal',
       'Revenue Category','AASIS Code', 'Cost Center', 'Designated','Earning', 'Employee Type', 'Fund', 'Job Profile',
       'Location', 'NACUBO Function', 'Pay Group', 'Pay Rate Type','Personnel Services Restrictions', 'Position', 'Deduction (Workday Owned)', 'Fringe Basis']
    result_df.drop(columns=columns_to_drop, inplace=True,errors='ignore')

    return result_df

if __name__ == '__main__':
    app.run(debug=True)
