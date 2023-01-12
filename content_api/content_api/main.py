"""
This script implements a very basic means of rendering tickets.
It's a hack to allow displaying non-static data in a reasonable 
fashiong using the Camunda 8 GUI.
"""

from fastapi import FastAPI
import logging


logging.basicConfig(level=logging.INFO)

app = FastAPI()

def load_template(name: str) -> str: 
    with open(f"./html/{name}", 'r', encoding="utf-8") as template_file:
        template = template_file.read()
    return template

from content_api.endpoints import *
