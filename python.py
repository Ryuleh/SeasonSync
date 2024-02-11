from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Replace with your API keys
EVENTBRITE_API_KEY = "QXCLS4X3FMQS3M3FVE"
GOOGLE_API_KEY = "AIzaSyDJ62yzREkfbxwiexRMlKeOpbsGz5dx56o"
# AIzaSyBopiP0KJOXuVCNeeKeP4jjkfnU7CLjpAE
# AIzaSyDJ62yzREkfbxwiexRMlKeOpbsGz5dx56o


def scrape_eventful_events(city):
    url = f"https://www.eventbrite.com/d/{city}/events/"
    response = requests.get(url)

    events = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        event_elements = soup.find_all("div", class_="listItem")

        for event_element in event_elements:
            event_name = event_element.find("span", class_="title").text.strip()
            event_date = event_element.find("span", class_="date").text.strip()
            event_location = event_element.find("span", class_="venue").text.strip()

            event_data = {
                "name": event_name,
                "date": event_date,
                "location": event_location,
            }
            events.append(event_data)

    return events


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/events", methods=["POST"])
def events():
    city = request.form["city"]

    # Use Google Maps API to get latitude and longitude of the city
    google_geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={GOOGLE_API_KEY}"
    google_geocode_response = requests.get(google_geocode_url).json()

    # Check if there are any results returned from the Google Maps API
    if (
        google_geocode_response["status"] != "OK"
        or len(google_geocode_response.get("results", [])) == 0
    ):
        return render_template("error.html", message="City not found")

    location = google_geocode_response["results"][0]["geometry"]["location"]
    latitude = location["lat"]
    longitude = location["lng"]

    # Use Eventbrite API to get events near the location
    eventbrite_url = "https://www.eventbriteapi.com/v3/events/search/"
    params = {
        "token": EVENTBRITE_API_KEY,
        "location.latitude": latitude,
        "location.longitude": longitude,
        "start_date.keyword": "this_spring,this_summer,this_fall,this_winter",
        "price": request.form.get("price", ""),
        "expand": "venue",  # Include venue information in the response
    }
    eventbrite_response = requests.get(eventbrite_url, params=params).json()
    events = eventbrite_response.get("events", [])

    # Web scrape Eventbrite for events
    eventbrite_events = scrape_eventful_events(city)

    return render_template("events.html", events=events + eventbrite_events)


@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query")

    # Use Google Maps API to get auto-suggestions for city names
    google_autocomplete_url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={query}&key={GOOGLE_API_KEY}"
    google_autocomplete_response = requests.get(google_autocomplete_url).json()
    predictions = google_autocomplete_response.get("predictions", [])
    suggestions = [prediction["description"] for prediction in predictions]

    return jsonify(suggestions=suggestions)


if __name__ == "__main__":
    app.run(debug=True)
