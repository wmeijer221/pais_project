import base64
from fastapi import HTTPException
from fastapi.responses import FileResponse
import imgkit
import math
import os
from PIL import Image
import random

from content_api.main import load_template, app, logger
from content_api.util import seconds_to_hours, seconds_to_hourminutes,\
                             PersistentObject, PersistentDict

ticket_template = load_template("ticket_template.html")
final_ticket_template = load_template("final_ticket_template.html")
ft_styles = load_template("ft_styles.css")

TICKET_ID_PATH = "./data/lt_latest.txt"
TICKET_PATH = "./data/lt_{order_id}.{ext}"

latest_ticket_id = PersistentObject(TICKET_ID_PATH)
latest_ticket: PersistentDict = None
latest_ticket_path = \
    TICKET_PATH.format(order_id = latest_ticket_id.get(), ext="json")
latest_ticket = PersistentDict(latest_ticket_path)

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
    data_path = TICKET_PATH.format(order_id = order_id, ext="json")
    latest_ticket = PersistentDict(data_path)
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
    logger.info(f'Loading tickets {order_id}.')
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
    ticket_files = []
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
            "departure_time": f"{seconds_to_hours(start_time):02d}:{seconds_to_hourminutes(start_time):02d}",
            "arrival_time": f"{seconds_to_hours(end_time) % 24 :02d}:{seconds_to_hourminutes(end_time):02d}",
        }
        start_time = end_time
        formatted_ticket = final_ticket_template.format(**data)
        formatted_ticket = ticket_template.format(formatted_ticket, ft_styles)

        # stores it.
        html_path = TICKET_PATH.format(order_id=order_id, ext="html")
        with open(html_path, "w+", encoding="utf-8") as output_file:
            output_file.write(formatted_ticket)
        output_file.close()
        ticket_id = f'{order_id}_{index}'
        img_path = TICKET_PATH.format(order_id=ticket_id, ext="png")
        imgkit.from_file(html_path, img_path, options={'quiet': ''})
        ticket_files.append(img_path)

    output_path = TICKET_PATH.format(order_id=order_id, ext="png")
    merge_as_grid(2, ticket_files, output_path)
    return output_path

def merge_as_grid(col_count: int, files: list[str], out_path: str):
    images = [Image.open(x) for x in files]
    width, height = 385, 285
    total_width = col_count * width
    total_height = math.ceil(len(files) / col_count) * height

    new_img = Image.new("RGB", (total_width, total_height))

    for index, img in enumerate(images):
        y_offset = math.floor(index / col_count) * height
        x_offset = (index % col_count) * width
        new_img.paste(img, (x_offset, y_offset))

    new_img.save(os.path.abspath(out_path))


def _generate_seat() -> str:
    seat = random.randint(1, 50)
    carriage = random.randint(1, 7)
    return f'Car {carriage}, Seat {seat:02d}'
