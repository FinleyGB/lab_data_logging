import os
import glob
import time
import csv
import pathlib
from datetime import datetime, timedelta
# from pi_config import pi_config

class TemperatureLogger:
    def __init__(self, config):
        self.config = config
        self.sensor_params = config['sensor_params']
        self.dir_params = config['temp_dir_params']
        
        # Base directory for DS18B20 sensors
        self.base_dir = self.sensor_params['SENSOR_DIR']
        
        # Default headers
        self.fields = ['Date (d/m/Y)', 'Time (H:M:S)', 'AOM (C)', 'SFG (C)', 'Spectro (C)', 'Cryo (C)']
        
        self._setup_drivers()
        # Find all sensor subfolders starting with '28'
        self.device_folders = glob.glob(os.path.join(self.base_dir, '28*'))
        self.device_files = [os.path.join(f, 'w1_slave') for f in self.device_folders]

    def _setup_drivers(self):
        """Load kernel modules for 1-wire communication."""
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

    def read_temp_ds18b20(self, device_file):
        """Reads and parses the raw temperature from the w1_slave file."""
        try:
            with open(device_file, 'r') as f:
                lines = f.readlines()
            
            # Wait for the sensor to indicate a valid 'YES' reading
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.5)
                with open(device_file, 'r') as f:
                    lines = f.readlines()

            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_str = lines[1][equals_pos+2:]
                return round(float(temp_str) / 1000, 2)
        except Exception as e:
            print(f"Error reading {device_file}: {e}")
            return None

    def get_weekly_filename(self):
        """Creates a filename based on the current week (Monday to Sunday)."""
        now = datetime.now()
        start = now - timedelta(days=now.weekday())
        end = start + timedelta(days=6)
        filename = f"{start.strftime('%Y_%m_%d')}_to_{end.strftime('%Y_%m_%d')}.csv"
        return os.path.join(self.dir_params['REMOTE_DIR'], filename)

    def log_session(self):
        """Main loop to read sensors and append to the weekly CSV."""
        max_attempts = self.sensor_params['MAX_ATTEMPTS']
        delay = self.sensor_params['DELAY']

        for attempt in range(1, max_attempts + 1):
            try:
                # 1. Ensure the directory exists
                pathlib.Path(self.dir_params['REMOTE_DIR']).mkdir(parents=True, exist_ok=True)
                
                data_file = self.get_weekly_filename()
                file_exists = os.path.exists(data_file)

                # 2. Collect sensor data
                sensor_data = [self.read_temp_ds18b20(f) for f in self.device_files]
                
                # 3. Construct the row
                new_row = [
                    datetime.now().strftime('%d/%m/%Y'), 
                    datetime.now().strftime('%H:%M:%S')
                ] + sensor_data

                # 4. Write to CSV (Fix: variable name is now consistently 'new_row')
                with open(data_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        # Write headers only if file is new
                        writer.writerow(self.fields)
                    writer.writerow(new_row)
                
                print(f"Successfully logged data: {new_row}")
                break 
            
            except Exception as e:
                print(f"Attempt {attempt} failed: {e}")
                if attempt == max_attempts:
                    self._send_critical_error(e)
                    raise
                time.sleep(delay)

    def _send_critical_error(self, error):
        """Handles Teams notifications on final failure."""
        try:
            import pymsteams
            # Use the webhook from your original script
            webhook = "https://heriotwatt.webhook.office.com/webhookb2/..." 
            myTeamsMessage = pymsteams.connectorcard(webhook)
            myTeamsMessage.text(f"Temp sensor error on Pi: {error}")
            myTeamsMessage.send()
        except Exception as notify_err:
            print(f"Could not send Teams alert: {notify_err}")

# if __name__ == '__main__':
#     logger = TemperatureLogger(pi_config)
#     logger.log_session()