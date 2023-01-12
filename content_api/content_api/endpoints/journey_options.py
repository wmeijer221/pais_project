from fastapi import HTTPException
from fastapi.responses import FileResponse
import imgkit
import json
import logging
import math
from os import path, mkdir

from content_api.main import load_template, app
from content_api.util import sum_values_of_key

LATEST_OPTION_PATH = "./data/option.dat"


ticket_template= load_template("ticket_template.html")
journey_template = load_template("journey_template.html")
leg_template = load_template("leg_template.html")
styles = load_template("styles.css")

if not path.exists("./data"):
    mkdir("./data")

try:
    with open(LATEST_OPTION_PATH, "r", encoding="utf-8") as option_file:
        latest_order_id = option_file.read().strip()
except:
    latest_order_id = "-1"

logging.info(f'Starting with {latest_order_id=}.')

@app.post("/set_latest_ticket_options")
async def set_latest_ticket(message: dict):
    global latest_order_id
    latest_order_id = message["order_id"]
    with open(LATEST_OPTION_PATH, "w+", encoding="utf-8") as option_file:
        option_file.write(str(latest_order_id))
    with open(f"./data/{latest_order_id}.json", "w+", encoding="utf-8") as data_file:
        options = message["route_options"]
        data_file.write(json.dumps(options, indent=4))


@app.get("/get_latest_ticket_options", response_class=FileResponse)
async def get_latest_ticket():
    global latest_order_id
    try:
        ticket_file = load_and_generate_options(latest_order_id)
        return FileResponse(ticket_file)
    except:
        raise HTTPException(status_code=404, detail="Ticket not found.")


@app.get("/get_ticket_options", response_class=FileResponse)
async def get_ticket_options(message: dict):
    order_id = message["order_id"]
    try:
        ticket_file = load_and_generate_options(order_id)
        return FileResponse(ticket_file)
    except:
        raise HTTPException(status_code=404, detail="Ticket not found.")


def load_and_generate_options(order_id: str) -> str:
    """
    Loads details of an order and generates an 
    image of all its journey options.
    """

    logging.info(f'Getting options for: {order_id}')
    ticket_options = load_options(order_id)
    ticket_file = generate_ticket(order_id, ticket_options)
    return ticket_file


def load_options(order_id: str) -> dict:
    """
    Loads the ticket options for an order.
    """

    data_path = f"./data/{order_id}.json"
    if not path.exists(data_path):
        return None
    with open(data_path, "r", encoding="utf-8") as data_file:
        data = data_file.read()
        options = json.loads(data)
    return options

def generate_ticket(order_id: str, ticket_options: dict) -> str:
    """
    Generates image of a ticket and returns its path.
    """

    html = generate_options_html(ticket_options)
    html_path = f'./data/{order_id}.html'
    with open(html_path, "w+", encoding="utf-8") as output_file:
        output_file.write(html)
    img_path = f'./data/{order_id}.png'
    imgkit.from_file(html_path, img_path)
    return img_path

def generate_options_html(options: dict) -> str:
    """
    Generates HTML for all journey options.
    """
    
    formatted_journeys = ""
    for journey_id, (key, option) in enumerate(options.items(), start=1):
        formatted_journey = generate_journey_html(journey_id, key, option)
        formatted_journeys = f'{formatted_journeys}{formatted_journey}'
    formatted_ticket = ticket_template.format(formatted_journeys, styles)
    return formatted_ticket

def generate_journey_html(journey_id: int, journey_key: str, journey: dict) -> str:
    """
    Generates HTML for a single journey option.
    """

    legs = journey["value"]

    formatted_legs = ""
    for leg_id, leg in enumerate(legs, start=1):
        formatted_leg = generate_leg_html(leg_id, leg)
        formatted_legs = f"{formatted_legs}{formatted_leg}"
    
    # TODO: assumes economy
    total_price = sum_values_of_key(legs, "price_eurocents_economy")
    total_time = sum_values_of_key(legs, "traveltime_seconds")

    journey_data = {
        "option_id": journey_id,
        "journey_id": journey_key,
        "start_station": legs[0]["start_station"],
        "end_station": legs[-1]["end_station"],
        "transfer_count": str(len(legs) - 1),
        "total_price": f'{(total_price / 100):.2f}',
        "total_hours": str(math.floor(total_time / 3600)),
        "total_minutes": str(math.floor((total_time % 3600) / 60)),
        "leg_details": formatted_legs
    }
    formatted_journey = journey_template.format(**journey_data)
    return formatted_journey


def generate_leg_html(leg_id: int, leg: dict) -> str:
    """
    Generates HTML for one leg of the journey.
    """

    leg_time = leg["traveltime_seconds"]
    params = {
        "leg_index": leg_id,
        "leg_start_station_name": leg["start_station"],
        "leg_end_station_name": leg["end_station"],
        "leg_duration_hours": str(math.floor(leg_time / 3600)),
        "leg_duration_minutes": str(math.floor((leg_time % 3600) / 60))
    }
    formatted_leg = leg_template.format(**params)
    return formatted_leg
