from flask import Flask, render_template, request, jsonify
import json
import requests

app = Flask(__name__)


# Function to get events from Eventbrite API
def get_events(city):
    # Use your Eventbrite API key here
    eventbrite_token = "LCRLH2GHRVPMF5YIR2P3"
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
    return (
        data["results"][0]["components"]["city"],
        data["results"][0]["components"]["country"],
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/events", methods=["GET", "POST"])
def events():
    if request.method == "POST":
        city = request.form["city"]
        events_data = get_events(city)
        city_name, country_name = get_location_details(city)
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
        with open("data.json", "w") as f:
            json.dump({"events": events_list}, f, indent=2)
        return render_template(
            "events.html", events=events_list, city=city_name, country=country_name
        )
    else:
        return render_template("events.html")


@app.route("/chat", methods=["POST"])
def chat():
    if request.method == "POST":
        message = request.form["message"]
        response = get_chatbot_response(message)
        return jsonify({"response": str(response)})


if __name__ == "__main__":
    app.run(debug=True)
