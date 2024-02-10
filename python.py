from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

# def get_events():
# url = api.com
# response = json.loads(requests.request("GET", url).text)
# event = response[]
# return response, event


# Sample data for seasonal events

seasonal_events = [
    {
        "name": "Spring Sale",
        "date": "March 20 - April 20",
        "description": "Get ready for spring with amazing discounts!",
    },
    {
        "name": "Summer Festival",
        "date": "June 21 - September 22",
        "description": "Join us for a summer celebration with live music, food, and activities!",
    },
    {
        "name": "Fall Harvest",
        "date": "September 23 - November 21",
        "description": "Celebrate the harvest season with farm-fresh produce and autumn-themed events.",
    },
    {
        "name": "Winter Wonderland",
        "date": "December 21 - March 19",
        "description": "Experience the magic of winter with festive decorations, ice skating, and holiday shopping.",
    },
]


@app.route("/")
def home():
    return render_template("index.html", seasonal_events=seasonal_events)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
    # app.run(debug=True)
