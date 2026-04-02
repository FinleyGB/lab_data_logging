from crontab import CronTab
from log_cryo_temp import pi_config

script_tag = pi_config['teams_params']['SCRIPT_TAG']

def resume_job(tag):
    cron = CronTab(user=True)
    jobs = list(cron.find_comment(tag))
    
    for job in jobs:
        # This removes the '#' from the job line
        job.enable(True)
        print(f"Resumed job: {job.command}")
    
    cron.write()

if __name__ == "__main__":
    resume_job(script_tag)