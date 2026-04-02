Temperature monitoring using DS18B20 sensors and a Raspberry pi.

Sensors utilize 1-wire communication standard and are wired in parallel.

Remote file transfer is done via sftp protocol. Network parameters are stored in the config file. 

New temp logs are created each week with file names indicating the start and end dates of that week.

example file name:

2026_03_30_to_2026_04_05.csv

repeat measurements are handled on the os level with crontab.

- To configure the cron job, run the script "schedule_temp_logging.py"
- To pause the cron, run the script "pause_temp_logging.py"
- To resume the cron, run the script "resume_temp_logging.py"

