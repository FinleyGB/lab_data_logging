from crontab import CronTab
from log_cryo_temp import pi_config

script_tag = pi_config['crontab_params']['SCRIPT_TAG']

def pause_job(tag):
    cron = CronTab(user=True)
    
    # Find all jobs with your specific tag
    jobs = list(cron.find_comment(tag))
    
    if not jobs:
        print(f"No job found with tag: {tag}")
        return

    for job in jobs:
        # This prepends a '#' to the job line
        job.enable(False)
        print(f"Paused job: {job.command}")
    
    cron.write()
    print("Crontab updated successfully.")

if __name__ == "__main__":
    pause_job(script_tag)