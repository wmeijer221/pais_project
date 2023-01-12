from fastapi import HTTPException
from fastapi.responses import FileResponse
import imgkit
import json
import logging
from os import path, mkdir

from content_api.main import load_template, app
from content_api.util import sum_values_of_key, seconds_to_hours, \
                             seconds_to_hourminutes, PersistentObject,\
                             PersistentDict

TICKET_ID_PATH = "./data/latest_ticket.dat"
TICKET_PATH = "./data/lt_{order_id}.json"

latest_ticket_id = PersistentObject(TICKET_ID_PATH)
latest_ticket: PersistentDict = None

@app.post("/set_latest_ticket")
async def set_latest_ticket(message: dict):
    global latest_ticket_id, latest_ticket
    order_id = str(message["order_id"])
    latest_ticket_id.set(order_id)
    path = TICKET_PATH.format(order_id = order_id)
    latest_ticket = PersistentDict(path)
    latest_ticket.set(message)

@app.get("/get_latest_ticket", response_class=FileResponse)
async def get_latest_ticket():
    global latest_ticket
    if latest_ticket is None or \
            not latest_ticket.is_defined():
        raise HTTPException(status_code=404, detail="Ticket not found.")
    try:
        ticket = latest_ticket.get()
        ticket_file = load_and_generate_ticket(ticket)
        return FileResponse(ticket_file)
    except:
        raise HTTPException(status_code=404, detail="Ticket not found.")

@app.get("/get_ticket/{order_id}", response_class=FileResponse)
async def get_latest_ticket(order_id: str):
    path = TICKET_PATH.format(order_id = order_id)
    ticket = PersistentDict(path)
    if not ticket.is_defined():
        raise HTTPException(status_code=404, detail="Ticket not found.")
    try:
        ticket = ticket.get()
        ticket_file = load_and_generate_ticket(ticket)
        return FileResponse(ticket_file)
    except:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    

def load_and_generate_ticket(ticket: dict) -> str:
    logging.info(f'Loading ticket {ticket["order_id"]}.')
    pass 
