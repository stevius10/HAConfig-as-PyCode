import os
import re
import time
from datetime import datetime, timedelta
import logging
from tqdm import tqdm
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError

LOCAL_FOLDER = "/share/Extern"
GOOGLE_DRIVE_FOLDER_ID = "1o4A8qbGa4pJ02tL72sa802RhESH3R96K"
TRASH_FOLDER_ID = "19q7mSrN0iFBhicZ6PESPgshyRFeuAQpe"
CREDENTIALS_FILE = "/homeassistant/.storage/google_assistant_auth.json"
LOG_FILE = "/config/scripts/.gdrive-sync.log"

logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s - %(message)s')

def truncate_log(log_file, lines_to_keep=10):
    with open(log_file, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        file.writelines(lines[-lines_to_keep:])
        
def list_local_folders():
    folders_to_sync = []
    for entry in os.listdir(LOCAL_FOLDER):
        full_path = os.path.join(LOCAL_FOLDER, entry)
        if os.path.isdir(full_path):
            if entry == '.Spotlight-V100':
                continue
            if entry.endswith(('Sicherungen', 'Medien')):
                continue
            folders_to_sync.append(full_path)
    return folders_to_sync
    
def create_folder(service, name, parent_id):
    query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields='files(id, name)').execute().get('files', [])

    for folder in results:
        if folder['name'] == name:
            return folder['id']

    # Falls kein passender Ordner gefunden wurde, erstelle einen neuen
    file_metadata = {
        'name': name,
        'parents': [parent_id],
        'mimeType': 'application/vnd.google-apps.folder'
    }
    try:
        folder = service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')
    except Exception as e:
        print(f"Fehler beim Erstellen des Ordners: {e}")
        return None

def upload_file(service, file_path, folder_id, trash_folder_id):
    file_name = os.path.basename(file_path)
    media = MediaFileUpload(file_path)
    
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    existing_files = service.files().list(q=query, fields='files(id, modifiedTime)').execute().get('files', [])

    if existing_files:
        existing_file = existing_files[0]
        existing_file_id = existing_file['id']
        existing_modified_time = existing_file['modifiedTime']

        local_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()

        if local_modified_time > existing_modified_time:
            try:
                file_metadata = {
                    'name': file_name,
                    'parents': [folder_id]
                }
                service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                move_to_trash(service, file_name, existing_file_id, trash_folder_id)
                print(f"[updated] {file_name} (from {existing_modified_time} to {local_modified_time}).")
            except HttpError as error:
                raise
        else:
            print(f"[skipped] {file_name} exists ({existing_modified_time}).")
    else:
        # Upload new file
        try:
            file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }
            service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f"[created] {file_name} ({os.path.getsize(file_path)}).")
        except HttpError as error:
            raise

def move_to_trash(service, file_name, file_path, trash_folder_id):
    file_metadata = {
        'name': file_name,
        'parents': [trash_folder_id]
    }
    service.files().copy(fileId=folder_id, body=file_metadata).execute()
    os.remove(file_path)
    print(f"[moved] {file_name} to trash.")

def delete_old_trash_files(service):
    seven_days_ago = datetime.now() - timedelta(days=7)
    query = f"'{TRASH_FOLDER_ID}' in parents and trashed=true and modifiedTime < '{seven_days_ago.isoformat()}'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    for file in results.get('files', []):
        service.files().delete(fileId=file['id']).execute()
        print(f"[deleted] {file['name']} from trash.")

def sync_folders(service):
    folders_to_sync = list_local_folders()
    for folder in folders_to_sync:
        folder_name = os.path.basename(folder)
        print(f"Syncing folder: {folder_name}")
        folder_id = create_folder(service, folder_name, GOOGLE_DRIVE_FOLDER_ID)
        sync_subfolders(service, folder, folder_id)

def sync_subfolders(service, folder_path, parent_folder_id):
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            dir_metadata = {
                'name': dir,
                'parents': [parent_folder_id],
                'mimeType': 'application/vnd.google-apps.folder'
            }
            new_dir = service.files().create(body=dir_metadata, fields='id').execute()
            sync_subfolders(service, os.path.join(root, dir), new_dir['id'])
        for file in tqdm(files, desc="Uploading files", unit="file"):
            file_path = os.path.join(root, file)
            upload_file(service, file_path, parent_folder_id, TRASH_FOLDER_ID)
    print(f"[completed] {os.path.basename(folder_path)}")

def main():
  
    truncate_log(LOG_FILE)
    
    # Authenticate with Google Drive
    creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
    scoped_creds = creds.with_scopes(['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=scoped_creds)

    print("Starting synchronization...")

    # Sync folders
    sync_folders(service)

    # Delete old trash files
    delete_old_trash_files(service)

    print("Synchronization completed.")

if __name__ == "__main__":
    main()