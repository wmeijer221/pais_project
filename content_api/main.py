"""
This script implements a very basic means of rendering tickets.
It's a hack to allow displaying non-static data in a reasonable 
fashiong using the Camunda 8 GUI.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
import logging
import imgkit
import math

logging.basicConfig(level=logging.INFO)

app = FastAPI()

def load_template(name: str) -> str: 
    with open(f"./html/{name}", 'r', encoding="utf-8") as template_file:
        template = template_file.read()
    return template

latest_option_id = "-1"
ticket_options = {}

ticket_template= load_template("ticket_template.html")
journey_template = load_template("journey_template.html")
leg_template = load_template("leg_template.html")
styles = load_template("styles.css")

@app.get("/get_latest_ticket_options", response_class=FileResponse)
async def get_latest_ticket():
    global latest_option_id
    logging.info(f'Getting options for: {latest_option_id}')
    ticket_file = generate_ticket(latest_option_id)
    if not ticket_file is None:
        return FileResponse(ticket_file)

def generate_ticket(order_id: str) -> str:
    """
    Generates image of a ticket.
    """

    global ticket_options

    if not order_id in ticket_options:
        return None

    latest_options = ticket_options[order_id]
    html = generate_html(latest_options)
    html_path = f'./data/{order_id}.html'
    with open(html_path, "w+", encoding="utf-8") as output_file:
        output_file.write(html)
    img_path = f'./data/{order_id}.png'
    imgkit.from_file(html_path, img_path)
    return img_path

def generate_html(options: dict) -> str:
    formatted_journeys = ""
    for journey_id, (key, option) in enumerate(options.items(), start=1):
        journey = option["value"]

        formatted_legs = ""
        for leg_id, leg in enumerate(journey, start=1):
            leg_time = leg["traveltime_seconds"]
            params = {
                "leg_index": leg_id,
                "leg_end_station_name": leg["start_station"],
                "leg_end_station_name": leg["end_station"],
                "leg_duration_hours": str(math.floor(leg_time / 3600)),
                "leg_duration_minutes": str(math.floor((leg_time % 3600) / 60))
            }
            formatted_leg = leg_template.format(**params)
            formatted_legs = f"{formatted_legs}{formatted_leg}"
        
        # TODO: assumes economy
        total_price = sum([leg["price_eurocents_economy"] for leg in journey])
        total_time = sum([leg["traveltime_seconds"] for leg in journey])
        journey_data = {
            "option_id": journey_id,
            "journey_id": key,
            "start_station": journey[0]["start_station"],
            "end_station": journey[-1]["end_station"],
            "transfer_count": str(len(journey) - 1),
            "total_price": f'{(total_price / 100):.2f}',
            "total_hours": str(math.floor(total_time / 3600)),
            "total_minutes": str(math.floor((total_time % 3600) / 60)),
            "leg_details": formatted_legs
        }
        formatted_journey = journey_template.format(**journey_data)
        formatted_journeys = f'{formatted_journeys}{formatted_journey}'
    formatted_ticket = ticket_template.format(formatted_journeys, styles)
    return formatted_ticket

@app.post("/set_latest_ticket_options")
async def set_latest_ticket(message: dict):
    global latest_option_id, ticket_options
    latest_option_id = message["order_id"]
    ticket_options[latest_option_id] = message["route_options"]
    