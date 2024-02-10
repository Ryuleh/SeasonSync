from flask import Flask, jsonify, request
from sqalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

def get_events():
  return jsonify({'events':events})

@app.route('/events', methods=['POST'])
def create_event():
  return jsonify({'message': 'Event created successfully'})

if __name__ == '__main__':
  app.run(debug=True)
  
  app.run()