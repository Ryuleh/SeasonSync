import requests
from flask import Flask, render_template, request

app = Flask(__name__)

EVENTBRITE_API_KEY = "LCRLH2GHRVPMF5YIR2P3"
OPENCAGE_API_KEY = "3a2e2407966344f4bd35adc2253b99da"


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
    try:
        lat = data["results"][0]["geometry"]["lat"]
        lng = data["results"][0]["geometry"]["lng"]
        return lat, lng
    except (IndexError, KeyError):
        # Handle cases where city is not found or API response does not contain expected data
        return None


def get_events_from_api(coordinates):
    if coordinates is None:
        return []  # Return empty list if coordinates are not available
    lat, lng = coordinates
    url = f"https://www.eventbriteapi.com/v3/events/search/?location.latitude={lat}&location.longitude={lng}&token={EVENTBRITE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    try:
        events = [
            {
                "name": event["name"]["text"],
                "description": event["description"]["text"],
                "date": event["start"]["local"],
                "location": event["venue"]["address"]["localized_address_display"],
            }
            for event in data.get("events", [])
        ]
        return events
    except KeyError:
        # Handle cases where API response does not contain events or there's an error
        return []


def apply_filters(events, form_data):
    # Implement filtering logic here if needed
    return events


if __name__ == "__main__":
    app.run(debug=True)
