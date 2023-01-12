import logging
import time

from .worker import create_client, run_loop
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

failed = True
time.sleep(10)
while failed: 
  try:
    create_client()
    from ticket_broker.use_cases import *
    logging.info("I started!")
    run_loop()
    failed = False
  except Exception as ex:
    logging.critical("Failed to run loop; retrying in 5 seconds.")
    logging.critical(ex)
    time.sleep(5)
