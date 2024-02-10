from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Define your function to get events from Eventbrite API
def get_events(city):
    eventbrite_token = "LCRLH2GHRVPMF5YIR2P3"
    url = f"https://www.eventbriteapi.com/v3/events/search/?q=&location.address={city}&token={eventbrite_token}"
    response = requests.get(url)
    data = response.json()
    events = data.get("events", [])
    return events

# Define an API route to get events by city
@app.route("/api/events", methods=["GET"])
def api_events():
    # Get city from query parameters
    city = request.args.get("city")

    # Check if city parameter is provided
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    # Get events for the specified city
    events = get_events(city)

    # Return the events as JSON response
    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True)
