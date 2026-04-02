from temp_logger_DS18B20 import TemperatureLogger
from remote_pi_config import pi_config

logger = TemperatureLogger(pi_config)

logger.log_session()