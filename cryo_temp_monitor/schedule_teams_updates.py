from crontab import CronTab
from log_cryo_temp import pi_config

# Access the crontab for the current user
cron = CronTab(user=True)

script_path = 'configure_teams_updates.py'
script_tag = 'cryo_temp_teams_msg'

# Create a new job
job = cron.new(command=f'python3 {script_path}', 
               comment=script_tag)

# Set the schedule (Every day at 2:30 AM)
job.minute.every(pi_config['teams_params']['update_freq'])

# Write the job to the real crontab
cron.write()