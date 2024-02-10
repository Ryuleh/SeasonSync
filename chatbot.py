from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import requests

app = Flask(__name__)

chatbot = ChatBot('MyChatBot')

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

def extract_keywords(user_input):
   
    keywords = user_input.split()
    return keywords

def get_events_based_on_keywords(keywords):
    response = requests.get(f"https://example.com/events?keywords={keywords}")
    data = response.json()
    return data

@app.route("/events", methods=["POST"])
def events():
    user_input = request.form["user_input"]

    bot_response = chatbot.get_response(user_input)

    if "events" in user_input:
        keywords = extract_keywords(user_input)
        events = get_events_based_on_keywords(keywords)
        return jsonify({"bot_response": bot_response, "events": events})
    else:
        return jsonify({"bot_response": bot_response})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
