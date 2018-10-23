import os
import requests

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = [{"channelname": "Default", "chats": [{"username": "richie", "message": "Welcome to the default room! Feel free to chat here or start a new channel", "timestamp": "23/10/2018 @ 09:25:00"}]}, {"channelname": "Main", "chats": [{"username": "bob", "message": "yo", "timestamp": "23/10/2018 @ 09:25:00"}]}]


@app.route("/")
def index():
    return render_template("index.html", channels=channels)

@app.route("/channel/<string:channelName>")
def channel(channelName):
    chatChannel = [item for item in channels if item["channelname"] == channelName]
    return render_template("channel.html", chatChannel=chatChannel)

@socketio.on("submit chat")
def chat(data):
    chatText = data["chatText"]
    channel = data["channel"]
    displayName = data["displayName"]
    timestamp = data["timestamp"]
    chatChannel = [item for item in channels if item["channelname"] == channel]
    if len(chatChannel[0]['chats']) >= 100:
    	del chatChannel[0]['chats'][0]
    chatChannel[0]['chats'].append({"username": displayName, "message": chatText, "timestamp": timestamp})
    emit("display chats", {"chatText": chatText, "displayName": displayName, "timestamp": timestamp}, broadcast=True)

@socketio.on("create room")
def create(data):
    channel = data["channel"]
    chatChannel = [item for item in channels if item["channelname"] == channel]
    if not chatChannel:
        channels.append({'channelname': channel, 'chats': []})
    emit("enter room", {"channel": channel}, broadcast=True)


