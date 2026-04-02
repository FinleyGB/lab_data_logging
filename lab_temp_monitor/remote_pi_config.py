"""
Config file for remote raspberry pi machine used for temperature logging.
"""

import os
from datetime import datetime

pi_config = dict(
    network_params = {'HOST':'100.88.110.107',
                      'PORT':22,
                      'USER':'jimmy-neutron',
                      'PASS':'Fruitflies1'
                      },
    
    temp_dir_params = {'REMOTE_DIR':'/home/jimmy-neutron/temp_logging',
                       'LOCAL_DIR':os.path.join(os.getcwd(),'temp_logging'),
                       'LOCAL_FOLDER_YEAR_NAME':f'{datetime.now().year}'},

    sensor_params = {'SENSOR_DIR':'/sys/bus/w1/devices/',
                     'MAX_ATTEMPTS':10,
                     'DELAY':5},

    crontab_params = {'MEASUREMENT_FREQ':60,
                      'PY_PATH':'/home/jimmy-neutron/miniconda3/bin/python3',
                      'SCRIPT_PATH':os.path.join(os.getcwd(),'setup_temp_logging.py'),
                      },
    
    teams_params = {'connector_card':"https://heriotwatt.webhook.office.com/webhookb2/36c66bd3-00f2-4593-9e53-9c5f95266f6b@6c425ff2-6865-42df-a4db-8e6af634813d/IncomingWebhook/97d2037215c54c3fa8eb01726c4e9d34/4665a5e6-0877-4796-b0de-b51e14e780be/V2OMZXlFjEVYfvc9z4WPZSMTbHBAIWuI6OP0rAyPbtXxQ1",
                    }
)