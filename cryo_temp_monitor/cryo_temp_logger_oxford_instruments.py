import platform
import os
import csv
import mySIM900
import mySIM922
import pymsteams
from datetime import datetime

class OxfordCryoLog:
    def __init__(self, config, port=None, slot=1):
        # 1. Hardware Initialization
        if port is None:
            port = 'COM5' if platform.system() == 'Windows' else '/dev/ttyUSB0'
        
        print(f"Connecting to SIM900 on {port}...")
        self.sim900 = mySIM900.Device(port, connection='serial')
        self.sim922 = mySIM922.Temp(self.sim900, slot)
        
        # 2. Config Extraction
        self.log_dir = config['temp_dir_params']['REMOTE_DIR']

        self.webhook_url = config['teams_params']['connector_card']
        self.title = config['teams_params']['title']
        
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        self.fields = ['Date (D/M/Y)', 'Time (H:M:S)', 'T1 (K)', 'T2 (K)', 'T3 (K)', 'T4 (K)']

    def get_temps(self):
        return self.sim922.get_temps()

    def log_to_csv(self, filename):
        filepath = os.path.join(self.log_dir, f"{filename}.csv")
        temps = self.get_temps()
        
        file_exists = os.path.isfile(filepath)
        now = datetime.now()
        new_row = [now.strftime('%d/%m/%Y'), now.strftime('%H:%M:%S')] + temps

        with open(filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(self.fields)
            writer.writerow(new_row)
        
        return temps

    def send_teams_status(self):
        """
        Sends a structured card to Teams using pymsteams.
        color: Hex code (default is a nice blue). Use "FF0000" for alerts.
        """
        try:
            teams_msg = pymsteams.connectorcard(self.webhook_url)
            teams_msg.title(self.title)
            teams_msg.text(f'Current temperature: {self.get_temps()}')
            teams_msg.send()
        except Exception as e:
            print(f"Teams notification failed: {e}")

    def close(self):
        if hasattr(self.sim900, 'mframe'):
            self.sim900.mframe.close()
            print('Device closed')

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
