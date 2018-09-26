import os
import requests

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = [{"channelname": "Default", "chats": [{"username": "richie", "message": "hi"}]}, {"channelname": "Main", "chats": [{"username": "bob", "message": "yo"}]}]


@app.route("/")
def index():
    return render_template("index.html", channels=channels)

@app.route("/channel/<string:channelName>")
def channel(channelName):
    chatChannel = [item for item in channels if item["channelname"] == channelName]
    return render_template("channel.html", chatChannel=chatChannel)

@socketio.on("submit chat")
def vote(data):
    chatText = data["chatText"]
    channel = data["channel"]
    displayName = data["displayName"]
    chatChannel = [item for item in channels if item["channelname"] == channel]
    print(chatChannel[0])
    print(chatChannel[0]['chats'])
    chatChannel[0]['chats'].append({"username": displayName, "message": chatText})
    emit("display chats", {"chatText": chatText, "displayName": displayName}, broadcast=True)
