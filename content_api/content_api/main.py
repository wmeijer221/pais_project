"""
This script implements a very basic means of rendering tickets.
It's a hack to allow displaying non-static data in a reasonable 
fashiong using the Camunda 8 GUI.
"""

from fastapi import FastAPI
import logging
from os import mkdir, path

from content_api._version import VERSION


logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

title = f"""
 _____ _     _       _      _          _____                     
|_   _|_|___| |_ ___| |_   | |_ ___   |   __|_ _ ___ ___ ___ ___ 
  | | | |  _| '_| -_|  _|  |  _| . |  |   __| | |  _| . | . | -_|
  |_| |_|___|_,_|___|_|    |_| |___|  |_____|___|_| |___|  _|___|
                                                        |_|      
                                                        
                                       Content API (v{VERSION})
"""
logger.info(title)

app = FastAPI()

if not path.exists("./data"):
    mkdir("./data")

def load_template(name: str) -> str: 
    with open(f"./html/{name}", 'r', encoding="utf-8") as template_file:
        template = template_file.read()
    return template

from content_api.endpoints import *
