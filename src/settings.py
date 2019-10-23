'''
    File name: settings.py
    Author: ZeroPass - Nejc Skerjanc
    License: MIT lincense
    Python Version: 3.6
'''

import logging

logging.basicConfig(level=logging.DEBUG) #waring, info, debug
logger = logging.getLogger(__name__)

config = {"database":
            {
            "user": "",
            "pass": "",
            "db" : ""
            },
         "registerTimeFrame" : 300 #5 minutes
}
