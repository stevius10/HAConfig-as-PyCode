from constants import GIT_REPO_URL, GIT_BRANCH_NAME, GIT_BRANCH_TARGET, \
  GIT_COMMIT_MESSAGE, GIT_CREDENTIALS_KEY, GIT_CREDENTIALS_CONFIG, \
  GOOGLE_DRIVE_LOCAL_FOLDER, GOOGLE_DRIVE_IGNORE_FOLDERS, \
  GOOGLE_DRIVE_REMOTE_FOLDER, GOOGLE_DRIVE_TRASH_FOLDER, \
  GOOGLE_DRIVE_CREDENTIALS_FILE, SERVICE_CRON_GOOGLE_DRIVE
from log import Log

import os
import io
import time
import re
import calendar
import datetime
import subprocess

from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

util = Log(pyscript.get_global_ctx())

@service
@time_trigger(SERVICE_CRON_GOGLE_DRIVE)
class Drive():
  
    os.environ["GOOGLE_DRIVE_IGNORE_FOLDERS"] = GOOGLE_DRIVE_IGNORE_FOLDERS
    
    def __init__(self, google_drive_credentials_file):
        creds = None
        credentials = Credentials.from_service_account_file(google_drive_credentials_file, scopes=["https://www.googleapis.com/auth/drive"])
        self.__service = build('drive', 'v3', credentials=credentials)
        self.google_drive_ignore_folders = os.environ.get('GOOGLE_DRIVE_IGNORE_FOLDERS') or GOOGLE_DRIVE_IGNORE_FOLDERS
    def list_files(self, folder_id):
        response = self.__service.files().list(
            q=f"'{folder_id}' in parents", fields='files(id,name,modifiedTime,mimeType,size)'
        ).execute()

        files_dict = {"all": response.get('files', []), "names": []}
        for item in files_dict['all']:
            if item['name'] not in self.google_drive_ignore_folders:
                files_dict['names'].append(item['name'])

        return files_dict

    def download_file(self, filename, local_path, file_id, update=False):
        local_path = f"{local_path}/{filename}"
        request = self.__service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            done = downloader.next_chunk()
        with open(local_path, 'wb') as out:
            out.write(fh.getbuffer())
        modified_time = self.__service.files().get(fileId=file_id, fields='modifiedTime').execute()['modifiedTime']
        modified_timestamp = Utils.convert_datetime_timestamp(modified_time)
        os.utime(local_path, (modified_timestamp, modified_timestamp))

        if update is not False:
            util.log("[local] updated {} ({})", filename, local_path)
        else:
            util.log("[local] {} ({})", filename, local_path)

    def upload_file(self, filename, local_path, folder_id, update=False):
        local_path = f"{local_path}/{filename}"
        modified_timestamp = Utils.get_local_file_timestamp(local_path)
        file_metadata = {
            'name': filename,
            'modifiedTime': Utils.convert_timestamp_datetime(modified_timestamp),
            'parents': [folder_id]
        }
        media = MediaFileUpload(local_path)
    
        try:
            existing_file = self.find_file_by_name(filename, folder_id)
    
            if existing_file:
                remote_modified_time = Utils.convert_datetime_timestamp(existing_file['modifiedTime'])
    
                if modified_timestamp > remote_modified_time:
                    uploaded_file = self.__service.files().update(fileId=existing_file['id'], media_body=media).execute()
                    util.log("[updated] {} from {} ({})", filename, Utils.get_local_file_timestamp(local_path), local_path)
                else:
                    util.log("[skipped] {}", filename)
            else:
                uploaded_file = self.__service.files().create(
                    body=file_metadata, media_body=media, fields='id'
                ).execute()
                util.log("[uploaded] {} ({})", filename, local_path)
    
            return uploaded_file if 'uploaded_file' in locals() else None
        except Exception as e:
            logger.error("Error uploading file: {}. Error: {}", filename, str(e))
            return False

    def find_file_by_name(self, filename, folder_id):
        response = self.__service.files().list(
            q=f"name='{filename}' and '{folder_id}' in parents", fields='files(id,name,modifiedTime)'
        ).execute()

        files = response.get('files', [])
        if files:
            return files[0]
        else:
            return None

    def compare_files(self, local_file_data, remote_file_data):
        modified = False
        if local_file_data['modifiedTime'] > remote_file_data['modifiedTime']:
            modified = 'local'
        elif local_file_data['modifiedTime'] < remote_file_data['modifiedTime']:
            modified = 'remote'
        return modified

    def upload_folder(self, foldername, folder_id):
        if foldername in google_drive_ignore_folders:
            util.log("[skipped] Ignored folder: {}", foldername)
            return False
        
        folder_metadata = {'name': foldername, 'parents': [folder_id], 'mimeType': 'application/vnd.google-apps.folder'}
        try:
            uploaded_folder = self.__service.files().create(body=folder_metadata).execute()
            util.log("[created] folder '{}'", uploaded_folder['name'])
            return uploaded_folder['id']
        except Exception as e:
            logger.error("Error creating folder: '{}'. Error: {}", folder_metadata["name"], str(e))
            return False
            
    def get_folder_size(self, folder_id):
        total_size = 0
        response = self.__service.files().list(
            q=f"'{folder_id}' in parents", fields='files(id,size,mimeType)', pageSize=1000
        ).execute()
    
        files = response.get('files', [])
        for file in files:
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                total_size += self.get_folder_size(file['id'])
            else:
                total_size += int(file.get('size', 0))
    
        return total_size

    def synchronize(self, local_path, folder_id, recursive=False):
        util.log("{} {}", "[sync] recursively" if recursive else "[sync]", local_path)
    
        if not os.path.exists(local_path):
            os.makedirs(local_path)
    
        queue = [(local_path, folder_id)]
    
        while queue:
            current_local_path, current_folder_id = queue.pop(0)
    
            drive_files = self.list_files(current_folder_id)
            local_files = Utils.list_local_files(current_local_path)
    
            drive_files_filtered = {
                'all': [file for file in drive_files['all'] if file['name'] not in IGNORE_FOLDERS],
                'names': [file['name'] for file in drive_files['all'] if file['name'] not in IGNORE_FOLDERS]
            }
    
            if current_local_path != local_path:
                drive_folder_size = self.get_folder_size(current_folder_id)
                local_folder_size = sum(os.path.getsize(os.path.join(current_local_path, f)) for f in local_files if os.path.isfile(os.path.join(current_local_path, f)))
                if drive_folder_size == local_folder_size:
                    util.log("[skipped] Folder size matches for {}", current_local_path)
                    continue
    
            same_files = list(set(drive_files_filtered['names']) & set(local_files))
    
            if len(same_files) == 0 and not recursive:
                util.log("[skipped] {}", current_local_path)
    
            for sm_file in same_files:
                local_path = f"{current_local_path}/{sm_file}"
    
                remote_file_data = next(
                    item for item in drive_files_filtered['all'] if item["name"] == sm_file
                )  
                remote_file_data["modifiedTime"] = Utils.convert_datetime_timestamp(remote_file_data["modifiedTime"])
    
                local_file_data = {}
                local_file_data["name"] = sm_file
                local_file_data["modifiedTime"] = Utils.get_local_file_timestamp(local_path)
    
                modified = self.compare_files(local_file_data, remote_file_data)
    
                if modified == 'local':
                    if os.path.isdir(local_path):
                        queue.append((local_path, remote_file_data['id']))
                    else:
                        self.upload_file(sm_file, current_local_path, current_folder_id, remote_file_data['id'])
    
                elif modified == 'remote':
                    if remote_file_data["mimeType"] == 'application/vnd.google-apps.folder':
                        queue.append((local_path, remote_file_data['id']))
                    else:
                        self.download_file(sm_file, current_local_path, remote_file_data['id'], True)
    
            different_files = list(set(drive_files_filtered['names']) ^ set(local_files))
    
            if len(different_files) == 0 and not recursive:
                util.log("[skipped] {}", current_local_path)
    
            for diff_file in different_files:
                if diff_file in drive_files_filtered['names']:
                    for remote_file in drive_files_filtered['all']:
                        if remote_file['name'] == diff_file:
                            if remote_file['mimeType'] == 'application/vnd.google-apps.folder':
                                local_path = f"{current_local_path}/{diff_file}"
                                queue.append((local_path, remote_file['id']))
                            else:
                                self.download_file(remote_file['name'], current_local_path, remote_file['id'])
    
                else:
                    local_path = f"{current_local_path}/{diff_file}"
                    if os.path.isdir(local_path):
                        created_folder_id = self.upload_folder(diff_file, current_folder_id)
                        if created_folder_id != False:
                            queue.append((local_path, created_folder_id))
                    else:
                        self.upload_file(diff_file, current_local_path, current_folder_id)
                        
class Utils():
    @classmethod
    def list_local_files(cls, local_path):
        return os.listdir(local_path)
    
    @classmethod
    def get_local_file_timestamp(cls, path):
        unix_timestamp = os.path.getmtime(path)
        utc_datetime = cls.convert_timestamp_datetime(unix_timestamp)
        utc_timestamp = cls.convert_datetime_timestamp(utc_datetime)
        return int(unix_timestamp)

    @classmethod
    def convert_datetime_timestamp(cls, date):
        date = re.sub(r'\.\d+', '', date)
        time_object = time.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        timestamp = calendar.timegm(time_object)
        return int(timestamp)

    @classmethod
    def convert_timestamp_datetime(cls, timestamp):
        datetime_object = datetime.utcfromtimestamp(timestamp)
        return datetime_object.isoformat("T") + "Z"

@service
def service_googledrive_sync():

    drive = Drive(google_drive_credentials_file=GOOGLE_DRIVE_CREDENTIALS_FILE)
    drive.synchronize(GOOGLE_DRIVE_LOCAL_FOLDER, GOOGLE_DRIVE_REMOTE_FOLDER)