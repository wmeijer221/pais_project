from fastapi import HTTPException
from fastapi.responses import FileResponse
import imgkit
import logging
import random
import base64

from content_api.main import load_template, app
from content_api.util import sum_values_of_key, seconds_to_hours, \
                             seconds_to_hourminutes, PersistentObject,\
                             PersistentDict

ticket_template = load_template("ticket_template.html")
final_ticket_template = load_template("final_ticket_template.html")
ft_styles = load_template("ft_styles.css")

TICKET_ID_PATH = "./data/latest_ticket.dat"
TICKET_PATH = "./data/lt_{order_id}.json"

latest_ticket_id = PersistentObject(TICKET_ID_PATH)
latest_ticket: PersistentDict = None
path = TICKET_PATH.format(order_id = latest_ticket_id.get())
latest_ticket = PersistentDict(path)

def load_image_as_base64_string(file_name: str) -> str:
    with open(file_name, "rb") as image_file: 
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string.decode("utf-8")

image_background = load_image_as_base64_string("./html/ticket.png")

@app.post("/get_ticket_template", response_class=FileResponse)
async def get_ticket_template():
    return FileResponse("./html/ticket.png")

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
    global latest_ticket, latest_ticket_id
    order_id = latest_ticket_id.get()
    try:
        ticket_file = load_and_generate_ticket(latest_ticket, order_id)
        headers = {'Cache-Control': 'no-cache'}
        return FileResponse(ticket_file, headers=headers)
    except Exception as ex:
        logging.info(ex)
        raise HTTPException(status_code=404, detail="Ticket not found.")

@app.get("/get_ticket/{order_id}", response_class=FileResponse)
async def get_latest_ticket(order_id: str):
    path = TICKET_PATH.format(order_id = order_id)
    ticket = PersistentDict(path)
    try:
        ticket_file = load_and_generate_ticket(ticket, order_id)
        headers = {'Cache-Control': 'no-cache'}
        return FileResponse(ticket_file, headers=headers)
    except:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    

def load_and_generate_ticket(ticket: PersistentDict, order_id: str) -> str:
    logging.info(f'Loading ticket {order_id}.')
    ticket_details = load_ticket_details(ticket)
    details = ticket_details["tickets"]
    ticket_path = generate_tickets(details, order_id)
    return ticket_path
    
def load_ticket_details(ticket: PersistentDict) -> dict:
    if not ticket.is_defined():
        raise Exception("Ticket not found.")
    return ticket.get()

def generate_tickets(tickets: list[dict], order_id: str) -> str:
    global image_background
    start_time = 32651
    logging.info(tickets)
    for index, ticket in enumerate(tickets):
        ticket_info = ticket["ticket"]
        traveler = ticket["traveler_information"]
        end_time = start_time + ticket_info["traveltime_seconds"]
        data = {
            "image_background": image_background,
            "station_from": ticket_info["start_station"],
            "station_to": ticket_info["end_station"],
            "traveler_name": traveler["full_name"],
            "traveler_seat": _generate_seat(),
            "departure_time": f"{seconds_to_hours(start_time)}:{seconds_to_hourminutes(start_time)}",
            "arrival_time": f"{seconds_to_hours(end_time)}:{seconds_to_hourminutes(end_time)}",
        }
        start_time = end_time
        formatted_ticket = final_ticket_template.format(**data)
        formatted_ticket = ticket_template.format(formatted_ticket, ft_styles)

        logging.info("FINISHED  FORMATTING")

        # stores it.
        html_path = f'./data/ft_{order_id}_{index}.html'
        with open(html_path, "w+", encoding="utf-8") as output_file:
            output_file.write(formatted_ticket)
        output_file.close()
        img_path = f'./data/ft_{order_id}_{index}.png'
        imgkit.from_file(html_path, img_path)

        logging.info("FINISHED STORING")


def _generate_seat() -> str:
    seat = random.randint(1, 50)
    carriage = random.randint(1, 7)
    return f'Car {carriage}, Seat {seat:02d}'
