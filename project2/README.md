# Project 2

Web Programming with Python and JavaScript

Project instructions are available [here](https://github.com/richardsa/CS50-Web-Programming-with-Python-and-Javascript/tree/master/project2).

This project allows users to chat in realtime using websockets (Flask-SocketIO in this case).

To run this Flask application:

1. Download the <code class="highlighter-rouge">project2</code> distribution code from https://github.com/richardsa/CS50-Web-Programming-with-Python-and-Javascript/raw/master/project2/project2.zip and unzip it.
2. In a terminal window, navigate into your project2 directory.
3. Run pip3 install -r requirements.txt in your terminal window to make sure that all of the necessary Python packages (Flask and Flask-SocketIO, for instance) are installed.
4. Set the environment variable FLASK_APP to be application.py. On a Mac or on Linux, the command to do this is export FLASK_APP=application.py. On Windows, the command is instead set FLASK_APP=application.py.
5. Run flask run to start up your Flask application.
6. If you navigate to the URL provided by flask, you should see the text Home Page with a listing of the default channels (Default and Main)
