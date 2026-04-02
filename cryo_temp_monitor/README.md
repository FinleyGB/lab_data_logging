Temperature monitoring for Oxford instruments using Serial to USB adaptor from SRS mainframe.

Remote file transfer is done via sftp protocol. Network parameters are stored in the config file. 

Remote file transfer is done via sftp protocol. Network parameters are stored in the config file. 

repeat measurements are handled on the os level with crontab.

- To configure the cron job, run the script "schedule_temp_logging.py"
- To pause the cron, run the script "pause_temp_logging.py"
- To resume the cron, run the script "resume_temp_logging.py"

Note on cron usage: once the cron job has been created. Do not use the "schedule_temp_logging.py" script again. Use the pause and resume. 

When cooling down cryostat overnight, one can use the teams update files to report the cryostat temp.

The following scripts must only be run on the raspberry pi:

- log_cryo_temp.py
- cryo_temp_logger_oxford_instruments.py
- schedule_temp_logging.py
- pause_temp_logging.py
- resume_temp_logging.py
- schedule_teams_updates.py
- pause_teams_updates.py
- resume_teams_updates.py