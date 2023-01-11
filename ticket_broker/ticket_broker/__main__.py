import logging

from .worker import run_loop
from ._version import VERSION

logging.basicConfig(level=logging.INFO)

title = f"""
 _____ _     _       _      _          _____                     
|_   _|_|___| |_ ___| |_   | |_ ___   |   __|_ _ ___ ___ ___ ___ 
  | | | |  _| '_| -_|  _|  |  _| . |  |   __| | |  _| . | . | -_|
  |_| |_|___|_,_|___|_|    |_| |___|  |_____|___|_| |___|  _|___|
                                                        |_|      
                                                        
                                       Ticket Broker (v{VERSION})
"""
logging.info(title)

run_loop()
