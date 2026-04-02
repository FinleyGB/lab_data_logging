from crontab import CronTab
from remote_pi_config import pi_config

# Access the crontab for the current user
cron = CronTab(user=True)

# Create a new job
job = cron.new(command=f'python3 {pi_config['crontab_params']['SCRIPT_PATH']}', 
               comment='my_script_tag')

# Set the schedule (Every day at 2:30 AM)
job.minute.every(1)

# Write the job to the real crontab
cron.write()