from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# Function to get events from Eventbrite API
def get_events(city):
    # Use your Eventbrite API key here
    eventbrite_token = (
        "https://www.eventbriteapi.com/v3/users/me/?token=LCRLH2GHRVPMF5YIR2P3"
    )
    url = f"https://www.eventbriteapi.com/v3/events/search/?q=&location.address={city}&token={eventbrite_token}"
    response = requests.get(url)
    data = response.json()
    events = data.get("events", [])
    return events


# Function to get location details from OpenCage API
def get_location_details(city):
    # Use your OpenCage API key here
    opencage_key = "3a2e2407966344f4bd35adc2253b99da"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={opencage_key}"
    response = requests.get(url)
    data = response.json()
    return data["results"][0]["geometry"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/events", methods=["GET", "POST"])
def events():
    if request.method == "POST":
        city = request.form["city"]
        events = get_events(city)
        location_details = get_location_details(city)
        return render_template("events.html", events=events, location=location_details)
    else:
        return render_template("events.html")


if __name__ == "__main__":
    app.run(debug=True)
