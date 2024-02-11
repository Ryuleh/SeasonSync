from flask import Flask, render_template, request
import requests

app = Flask(__name__)

EVENTBRITE_API_KEY = "LCRLH2GHRVPMF5YIR2P3"
OPENCAGE_API_KEY = "1a1e67bfc2e24b81adfa6a86b5e3104a"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/events", methods=["POST"])
def get_events():
    city = request.form["city"]
    coordinates = get_coordinates(city)
    events = get_events_from_api(coordinates)
    filtered_events = apply_filters(events, request.form)
    return render_template("events.html", events=filtered_events)


def get_coordinates(city):
    url = (
        f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={OPENCAGE_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    lat = data["results"][0]["geometry"]["lat"]
    lng = data["results"][0]["geometry"]["lng"]
    return lat, lng


def get_events_from_api(coordinates):
    lat, lng = coordinates
    url = f"https://www.eventbriteapi.com/v3/events/search/?location.latitude={lat}&location.longitude={lng}&token={EVENTBRITE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    events = []
    for event in data["events"]:
        event_info = {
            "name": event["name"]["text"],
            "description": event["description"]["text"],
            "date": event["start"]["local"],
            "location": event["venue"]["address"]["localized_address_display"],
        }
        events.append(event_info)
    return events


def apply_filters(events, form_data):
    filtered_events = []
    for event in events:
        # Check if event is within the desired season
        # Check if event is free or paid
        # Check if event duration matches user preference
        filtered_events.append(event)  # Temporarily, no filtering applied
    return filtered_events


if __name__ == "__main__":
    app.run(debug=True)
