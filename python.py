from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)


def get_events(city):
    eventbrite_token = "LCRLH2GHRVPMF5YIR2P3"
    url = f"https://www.eventbriteapi.com/v3/events/search/?q=&location.address={city}&token={eventbrite_token}"
    response = requests.get(url)
    data = response.json()
    events = data.get("events", [])
    return events


def get_location_details(city):
    opencage_key = "3a2e2407966344f4bd35adc2253b99da"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={opencage_key}"
    response = requests.get(url)
    data = response.json()
    if data["results"]:
        return (
            data["results"][0]["components"]["city"],
            data["results"][0]["components"]["country"],
        )
    else:
        return None, None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/events", methods=["GET", "POST"])
def events():

    if request.method == "POST":
        city = request.form["city"]
        city_name, country_name = get_location_details(city)
        if city_name:
            events_data = get_events(city)
            if events_data:
                events_list = []
                for event in events_data:
                    event_details = {
                        "name": event["name"]["text"],
                        "description": event["description"]["text"],
                        "start_date": event["start"]["local"],
                        "end_date": event["end"]["local"],
                        "location": {
                            "name": event["venue"]["name"],
                            "latitude": event["venue"]["latitude"],
                            "longitude": event["venue"]["longitude"],
                        },
                        "url": event["url"],
                        "city": city_name,
                        "country": country_name,
                    }
                    events_list.append(event_details)
                return render_template(
                    "events",
                    events=events_list,
                    city=city_name,
                    country=country_name,
                )
            else:
                return render_template(
                    "error.html", message="No events found for this city."
                )
