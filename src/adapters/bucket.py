import boto3
import tempfile
import os


class Bucket:

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = boto3.client('s3')

    def upload_file(self, file_path, key):
        self.client.upload_file(
            file_path,
            self.bucket_name,
            key
        )
        return key

    def download_file(self, key, file_path: str = None):
        if not file_path:
            file_path = tempfile.mktemp()
            file_path = file_path + key.split("/")[-1]
        self.client.download_file(
            self.bucket_name,
            key,
            file_path
        )
        return file_path

    def download_multiple_keys(self, keys):
        temp_dir = tempfile.mkdtemp()
        files = []
        for key in keys:
            file = self.download_file(key, f'{temp_dir}/{key.split("/")[-1]}')
            files.append(file)
        return files

    def list_files(self, prefix):
        response = self.client.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=prefix
        )
        return response.get('Contents', [])

    def sync_folder(self, local_folder, remote_folder):
        for root, _, files in os.walk(local_folder):
            for file in files:
                local_file = os.path.join(root, file)
                remote_file = os.path.join(remote_folder, file)
                self.upload_file(local_file, remote_file)
            # Remove files in remote folder that are not in local folder
            remote_files = self.list_files(remote_folder)
            remote_files = [f['Key'] for f in remote_files]
            for remote_file in remote_files:
                if remote_file not in [os.path.join(remote_folder, f) for f in files]:
                    self.client.delete_object(
                        Bucket=self.bucket_name,
                        Key=remote_file
                    )
        return True

    def delete_directory(self, directory):
        files_in_directory = self.list_files(directory)
        for file in files_in_directory:
            print(f"Deleting {file['Key']}")
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=file['Key']
            )
        return True
