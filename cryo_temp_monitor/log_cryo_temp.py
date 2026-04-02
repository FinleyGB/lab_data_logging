from cryo_temp_logger_oxford_instruments import OxfordCryoLog
from remote_pi_config import pi_config

cryo = OxfordCryoLog(pi_config)

fname = pi_config['temp_dir_params']['fname']

cryo.log_to_csv(fname)