from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

# Eventbrite API key
EVENTBRITE_API_KEY = "LCRLH2GHRVPMF5YIR2P3"

# OpenCage API key
OPENCAGE_API_KEY = "3a2e2407966344f4bd35adc2253b99da"


# Function to get current season based on month
def get_season():
    month = datetime.datetime.now().month
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "fall"


# Function to get latitude and longitude coordinates for a city using OpenCage API
def get_coordinates(city):
    url = (
        f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={OPENCAGE_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    if data["results"]:
        lat = data["results"][0]["geometry"]["lat"]
        lng = data["results"][0]["geometry"]["lng"]
        return lat, lng
    else:
        return None, None


# Function to search for seasonal events using Eventbrite API
def search_events(lat, lng, season):
    url = "https://www.eventbriteapi.com/v3/events/search/"
    params = {
        "location.latitude": lat,
        "location.longitude": lng,
        "location.within": "10km",  # Search within 10km radius
        "start_date.keyword": season,
        "price": "free",  # Filter for free events
        "date.keyword": "today",  # Filter for events happening today
    }
    headers = {"Authorization": f"Bearer {EVENTBRITE_API_KEY}"}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    events = []
    if "events" in data:
        for event in data["events"]:
            event_details = {
                "name": event["name"]["text"],
                "start_time": event["start"]["local"],
                "end_time": event["end"]["local"],
                "url": event["url"],
            }
            events.append(event_details)
    return events


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        city = request.form["city"]
        lat, lng = get_coordinates(city)
        if lat and lng:
            season = get_season()
            events = search_events(lat, lng, season)
            return jsonify({"events": events})
        else:
            return jsonify({"message": "City not found"}), 404
    else:
        return """
            <form method="post">
                <label for="city">Enter your city:</label><br>
                <input type="text" id="city" name="city"><br>
                <input type="submit" value="Submit">
            </form>
        """


if __name__ == "__main__":
    app.run(debug=True)
