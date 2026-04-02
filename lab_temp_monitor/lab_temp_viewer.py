import matplotlib.pyplot as plt
import pandas as pd
import os
import re
from datetime import datetime

from lab_temp_monitor.remote_pi_config import pi_config

data_path = os.path.join(pi_config['temp_params']['LOCAL_DIR'],pi_config['temp_params']['LOCAL_FOLDER'])

def get_latest_local_file(folder_path):
    # Get all files in the specified directory
    try:
        all_files = os.listdir(folder_path)
    except FileNotFoundError:
        print("The specified path does not exist.")
        return None

    file_dates = []

    for filename in all_files:
        # Regex to find YYYY_MM_DD
        match = re.search(r'(\d{4}_\d{2}_\d{2})', filename)
        if match:
            try:
                # Convert string to date object
                file_date = datetime.strptime(match.group(1), "%Y_%m_%d")
                file_dates.append((file_date, filename))
            except ValueError:
                continue

    if not file_dates:
        return None

    # Find the tuple with the latest date
    latest_date, latest_filename = max(file_dates, key=lambda x: x[0])
    
    # Return the full path to the file
    return os.path.join(folder_path, latest_filename)

latest_file = get_latest_local_file(data_path)


# Load your data (example)
df = pd.read_csv(latest_file)

# Combine the first two columns into a single 'Timestamp'
# We use .astype(str) to ensure they are treated as text during concatenation
df['Timestamp'] = pd.to_datetime(df.iloc[:, 0].astype(str) + ' ' + df.iloc[:, 1].astype(str))

# Set the Timestamp as the index for easier plotting
df.set_index('Timestamp', inplace=True)

# Create the plot
plt.figure(figsize=(12, 6))

# Plot each column
plt.plot(df.index, df['SFG (C)'], label='SFG')
plt.plot(df.index, df['AOM (C)'], label='AOM')
plt.plot(df.index, df['Cryo (C)'], label='Cryo')
plt.plot(df.index, df['Spectro (C)'], label='Spectro')

# Formatting
plt.title('System Temperature Monitoring')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# Auto-format the dates on the x-axis to prevent overlapping
plt.gcf().autofmt_xdate()

plt.show()