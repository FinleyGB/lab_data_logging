import os
import re
import paramiko
import pathlib
from datetime import datetime
# from remote_pi_config import pi_config

class PiFileTransfer:
    def __init__(self, config):
        """Initialize parameters from the config dictionary."""
        self.host = config['network_params']['HOST']
        self.port = config['network_params']['PORT']
        self.user = config['network_params']['USER']
        self.password = config['network_params']['PASS']
        
        self.remote_dir = config['temp_dir_params']['REMOTE_DIR']
        self.local_root = config['temp_dir_params']['LOCAL_DIR']
        self.year_folder = config['temp_dir_params']['LOCAL_FOLDER_YEAR_NAME']
        
        self.ssh = None
        self.sftp = None

        self.connect()

    def connect(self):
        """Establish SSH and SFTP connections."""
        # print(f"Connecting to {self.host}...")
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, self.port, self.user, self.password)
        self.sftp = self.ssh.open_sftp()
        print(f'Connection to {self.host} successful!')

    def close(self):
        """Close connections safely."""
        if self.sftp:
            self.sftp.close()
        if self.ssh:
            self.ssh.close()
        print(f"Connection to {self.host} closed.")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def is_today_in_filename(self, filename):
        """Checks if today's date falls within the range specified in the filename."""
        today = datetime.now().date()
        date_strings = re.findall(r'\d{4}_\d{2}_\d{2}', filename)
        
        if len(date_strings) < 2:
            return False
        
        try:
            start_date = datetime.strptime(date_strings[0], "%Y_%m_%d").date()
            end_date = datetime.strptime(date_strings[1], "%Y_%m_%d").date()
            return start_date <= today <= end_date
        except ValueError as e:
            print(f"Error parsing dates in {filename}: {e}")
            return False

    def sync_files(self, delete_on_remote=False):
        """Main logic to download files and optionally clean up remote storage."""
        # 1. Ensure local directory exists
        local_target_dir = os.path.join(self.local_root, self.year_folder)
        pathlib.Path(local_target_dir).mkdir(parents=True, exist_ok=True)
        print(f"Saving to: {local_target_dir}")

        # 2. List remote files
        files = self.sftp.listdir(self.remote_dir)
        # print(f"Found {len(files)} files in {self.remote_dir}")

        for file in files:
            remote_file_path = os.path.join(self.remote_dir, file)
            local_file_path = os.path.join(local_target_dir, file)
            
            in_progress = self.is_today_in_filename(file)
            
            # Download file
            print(f"Downloading {file}...")
            self.sftp.get(remote_file_path, local_file_path)

            if in_progress:
                print(f"-> {file}: Recording still in progress. Keeping on Pi.")
            else:
                print(f"-> {file}: Transfer complete.")
                if delete_on_remote:
                    self.sftp.remove(remote_file_path)
                    print(f"-> {file}: Removed from Pi to free up space.")

# # --- Execution Block ---
# if __name__ == '__main__':
#     try:
#         # Using 'with' handles connect() and close() automatically
#         with PiFileTransfer(pi_config) as client:
#             client.sync_files(delete_on_remote=False) # Set to True to enable cleanup
#     except Exception as e:
#         print(f"An error occurred: {e}")