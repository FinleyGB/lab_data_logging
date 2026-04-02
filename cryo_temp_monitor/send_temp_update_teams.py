from cryo_temp_logger_oxford_instruments import OxfordCryoLog
from remote_pi_config import pi_config

cryo = OxfordCryoLog(pi_config)

cryo.send_teams_status()