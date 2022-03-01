# -*- coding: utf-8 -*-
"""bitcoin prediction for next 30 days

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11Iwb35DgziR_D4_KTCk5wa5qLHHUA-mi

This notebook provides recipes for loading and saving data from external sources.
"""

import pandas  as pd
from fbprophet import Prophet

from google.colab import files
upload=files.upload()
upload

import io
df=pd.read_csv(io.BytesIO(upload['bitcoin.csv']))
df

df=df[["Date","Close"]]
df
df.columns=["ds","y"]
df

prophet=Prophet()
prophet.fit(df)

future=prophet.make_future_dataframe(periods=365)
future

forecast=prophet.predict(future)
forecast[["ds","yhat","yhat_lower","yhat_upper"]].tail(200)

from fbprophet.plot import plot
prophet.plot(forecast, figsize=(20,10))

"""# Local file system

## Uploading files from your local file system

<code>files.upload</code> returns a dictionary of the files which were uploaded.
The dictionary is keyed by the file name and values are the data which were uploaded.
"""

from google.colab import files

uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))

"""## Downloading files to your local file system

<code>files.download</code> will invoke a browser download of the file to your local computer.

"""

from google.colab import files

with open('example.txt', 'w') as f:
  f.write('some content')

files.download('example.txt')

"""# Google Drive

You can access files in Drive in a number of ways, including:
- Mounting your Google Drive in the runtime's virtual machine
- Using a wrapper around the API such as <a href="https://pythonhosted.org/PyDrive/">PyDrive</a>
- Using the <a href="https://developers.google.com/drive/v3/web/about-sdk">native REST API</a>



Examples of each are below.

## Mounting Google Drive locally

The example below shows how to mount your Google Drive on your runtime using an authorisation code, and how to write and read files there. Once executed, you will be able to see the new file &#40;<code>foo.txt</code>&#41; at <a href="https://drive.google.com/">https://drive.google.com/</a>.

This only supports reading, writing and moving files; to programmatically modify sharing settings or other metadata, use one of the other options below.

<strong>Note:</strong> When using the 'Mount Drive' button in the file browser, no authentication codes are necessary for notebooks that have only been edited by the current user.
"""

from google.colab import drive
drive.mount('/content/drive')

with open('/content/drive/My Drive/foo.txt', 'w') as f:
  f.write('Hello Google Drive!')
!cat /content/drive/My\ Drive/foo.txt

drive.flush_and_unmount()
print('All changes made in this colab session should now be visible in Drive.')

"""## PyDrive

The examples below demonstrate authentication and file upload/download using PyDrive. More examples are available in the <a href="https://pythonhosted.org/PyDrive/">PyDrive documentation</a>.
"""

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

"""Authenticate and create the PyDrive client.

"""

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

"""Create and upload a text file.

"""

uploaded = drive.CreateFile({'title': 'Sample upload.txt'})
uploaded.SetContentString('Sample upload file content')
uploaded.Upload()
print('Uploaded file with ID {}'.format(uploaded.get('id')))

"""Load a file by ID and print its contents.

"""

downloaded = drive.CreateFile({'id': uploaded.get('id')})
print('Downloaded content "{}"'.format(downloaded.GetContentString()))

"""## Drive REST API

In order to use the Drive API, we must first authenticate and construct an API client.

"""

from google.colab import auth
auth.authenticate_user()
from googleapiclient.discovery import build
drive_service = build('drive', 'v3')

"""With this client, we can use any of the functions in the <a href="https://developers.google.com/drive/v3/reference/">Google Drive API reference</a>. Examples follow.

### Creating a new Drive file with data from Python

First, create a local file to upload.
"""

with open('/tmp/to_upload.txt', 'w') as f:
  f.write('my sample file')

print('/tmp/to_upload.txt contains:')
!cat /tmp/to_upload.txt

"""Upload it using the <a href="https://developers.google.com/drive/v3/reference/files/create"><code>files.create</code></a> method. Further details on uploading files are available in the <a href="https://developers.google.com/drive/v3/web/manage-uploads">developer documentation</a>."""

from googleapiclient.http import MediaFileUpload

file_metadata = {
  'name': 'Sample file',
  'mimeType': 'text/plain'
}
media = MediaFileUpload('/tmp/to_upload.txt', 
                        mimetype='text/plain',
                        resumable=True)
created = drive_service.files().create(body=file_metadata,
                                       media_body=media,
                                       fields='id').execute()
print('File ID: {}'.format(created.get('id')))

"""After executing the cell above, you will see a new file named 'Sample file' at <a href="https://drive.google.com/">https://drive.google.com/</a>.

### Downloading data from a Drive file into Python

Download the file that we uploaded above.
"""

file_id = created.get('id')

import io
from googleapiclient.http import MediaIoBaseDownload

request = drive_service.files().get_media(fileId=file_id)
downloaded = io.BytesIO()
downloader = MediaIoBaseDownload(downloaded, request)
done = False
while done is False:
  # _ is a placeholder for a progress object that we ignore.
  # (Our file is small, so we skip reporting progress.)
  _, done = downloader.next_chunk()

downloaded.seek(0)
print('Downloaded file contents are: {}'.format(downloaded.read()))

"""In order to download a different file, set <code>file&#95;id</code> above to the ID of that file, which will look like '1uBtlaggVyWshwcyP6kEI-y&#95;W3P8D26sz'.

# Google Sheets

Our examples below use the open source <a href="https://github.com/burnash/gspread"><code>gspread</code></a> library for interacting with Google Sheets.

Import the library, authenticate and create the interface to Sheets.
"""

from google.colab import auth
auth.authenticate_user()

import gspread
from oauth2client.client import GoogleCredentials

gc = gspread.authorize(GoogleCredentials.get_application_default())

"""Below is a small set of <code>gspread</code> examples. Additional examples are available at the <a href="https://github.com/burnash/gspread#more-examples"><code>gspread</code> GitHub page</a>.

## Creating a new sheet with data from Python
"""

sh = gc.create('My cool spreadsheet')

"""After executing the cell above, you will see a new spreadsheet named 'My cool spreadsheet' at <a href="https://sheets.google.com/">https://sheets.google.com</a>.

Open our new sheet and add some random data.
"""

worksheet = gc.open('My cool spreadsheet').sheet1

cell_list = worksheet.range('A1:C2')

import random
for cell in cell_list:
  cell.value = random.randint(1, 10)

worksheet.update_cells(cell_list)

"""## Downloading data from a sheet into Python as a Pandas DataFrame

Read back the random data that we inserted above and convert the result into a <a href="https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html">Pandas DataFrame</a>.
"""

worksheet = gc.open('My cool spreadsheet').sheet1

# get_all_values gives a list of rows.
rows = worksheet.get_all_values()
print(rows)

import pandas as pd
pd.DataFrame.from_records(rows)

"""# Google Cloud Storage &#40;GCS&#41;

In order to use Colaboratory with GCS, you'll need to create a <a href="https://cloud.google.com/storage/docs/projects">Google Cloud project</a> or use a pre-existing one.

Specify your project ID below:
"""

project_id = 'Your_project_ID_here'

"""Files in GCS are contained in <a href="https://cloud.google.com/storage/docs/key-terms#buckets">buckets</a>.

Buckets must have a globally unique name, so we generate one here.
"""

import uuid
bucket_name = 'colab-sample-bucket-' + str(uuid.uuid1())

"""In order to access GCS, we must authenticate."""

from google.colab import auth
auth.authenticate_user()

"""GCS can be accessed via the <code>gsutil</code> command-line utility or via the native Python API.

## `gsutil`

First, we configure <code>gsutil</code> to use the project that we specified above by using <code>gcloud</code>.
"""

!gcloud config set project {project_id}

"""Create a local file to upload."""

with open('/tmp/to_upload.txt', 'w') as f:
  f.write('my sample file')

print('/tmp/to_upload.txt contains:')
!cat /tmp/to_upload.txt

"""Make a bucket to which we'll upload the file &#40;<a href="https://cloud.google.com/storage/docs/gsutil/commands/mb">documentation</a>&#41;."""

!gsutil mb gs://{bucket_name}

"""Copy the file to our new bucket &#40;<a href="https://cloud.google.com/storage/docs/gsutil/commands/cp">documentation</a>&#41;."""

!gsutil cp /tmp/to_upload.txt gs://{bucket_name}/

"""Dump the contents of our newly copied file to make sure that everything worked &#40;<a href="https://cloud.google.com/storage/docs/gsutil/commands/cat">documentation</a>&#41;.

"""

!gsutil cat gs://{bucket_name}/to_upload.txt

#@markdown Once the upload has finished, the data will appear in the Cloud Console storage browser for your project:
print('https://console.cloud.google.com/storage/browser?project=' + project_id)

"""Finally, we'll download the file that we just uploaded in the example above. It's as simple as reversing the order in the <code>gsutil cp</code> command."""

!gsutil cp gs://{bucket_name}/to_upload.txt /tmp/gsutil_download.txt
  
# Print the result to make sure that the transfer worked.
!cat /tmp/gsutil_download.txt

"""## Python API

These snippets based on <a href="https://github.com/GoogleCloudPlatform/storage-file-transfer-json-python/blob/master/chunked_transfer.py">a larger example</a> that shows additional uses of the API.

First, we create the service client.
"""

from googleapiclient.discovery import build
gcs_service = build('storage', 'v1')

"""Create a local file to upload."""

with open('/tmp/to_upload.txt', 'w') as f:
  f.write('my sample file')

print('/tmp/to_upload.txt contains:')
!cat /tmp/to_upload.txt

"""Create a bucket in the project specified above."""

# Use a different globally unique bucket name from the gsutil example above.
import uuid
bucket_name = 'colab-sample-bucket-' + str(uuid.uuid1())

body = {
  'name': bucket_name,
  # For a full list of locations, see:
  # https://cloud.google.com/storage/docs/bucket-locations
  'location': 'us',
}
gcs_service.buckets().insert(project=project_id, body=body).execute()
print('Done')

"""Upload the file to our newly created bucket."""

from googleapiclient.http import MediaFileUpload

media = MediaFileUpload('/tmp/to_upload.txt', 
                        mimetype='text/plain',
                        resumable=True)

request = gcs_service.objects().insert(bucket=bucket_name, 
                                       name='to_upload.txt',
                                       media_body=media)

response = None
while response is None:
  # _ is a placeholder for a progress object that we ignore.
  # (Our file is small, so we skip reporting progress.)
  _, response = request.next_chunk()

print('Upload complete')

#@markdown Once the upload has finished, the data will appear in the Cloud Console storage browser for your project:
print('https://console.cloud.google.com/storage/browser?project=' + project_id)

"""Download the file that we just uploaded."""

from apiclient.http import MediaIoBaseDownload

with open('/tmp/downloaded_from_gcs.txt', 'wb') as f:
  request = gcs_service.objects().get_media(bucket=bucket_name,
                                            object='to_upload.txt')
  media = MediaIoBaseDownload(f, request)

  done = False
  while not done:
    # _ is a placeholder for a progress object that we ignore.
    # (Our file is small, so we skip reporting progress.)
    _, done = media.next_chunk()

print('Download complete')

"""Inspect the downloaded file.

"""

!cat /tmp/downloaded_from_gcs.txt