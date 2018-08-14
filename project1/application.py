import os
import requests
from flask import Flask, render_template, request, session, jsonify, redirect, Markup, url_for, flash
from flask_session import Session
from flask_sslify import SSLify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
sslify = SSLify(app)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Check for environment variable
if not os.getenv("GOODREADS_KEY"):
    raise RuntimeError("GOODREADS_KEY is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("search.html")

@app.route("/books/<int:book_id>")
def book(book_id):
    userReview = ''
    # Make sure book exists.
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    if book is None:
        return render_template("error.html", message="No such book.")
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": os.getenv("GOODREADS_KEY"), "isbns": book['isbn']})
    bookDict = res.json()
    gbook = bookDict.get('books')
    reviews = db.execute("SELECT * FROM reviews JOIN usertable on usertable.id = user_id WHERE book_id = :book_id", {"book_id": book_id}).fetchall();
    if session.get('user_id'):
        user_id = session.get('user_id')
        userReview = db.execute("SELECT * FROM reviews WHERE book_id = :book_id and user_id = :user_id", {"book_id": book_id, "user_id": user_id}).fetchall();
    return render_template("book.html", book=book, gbook=gbook, reviews=reviews, userReview=userReview)

@app.route("/api/<string:book_isbn>")
def apiRes(book_isbn):
    # Make sure book exists.
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": book_isbn}).fetchone()
    if book is None:
        return jsonify('No book with that isbn exists')
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "Vf6o1vG8MZ48NSMMDn622A", "isbns": book['isbn']})
    bookDict = res.json()
    gbook = bookDict.get('books')
    class Object1(object):
        pass

    apiRes = {}
    apiRes["title"] = book['title']
    apiRes["author"] = book["author"]
    apiRes["year"] = book["year"]
    apiRes["isbn"]  = book['isbn']
    apiRes["review_count"] = gbook[0]["work_ratings_count"]
    apiRes["average_score"] = gbook[0]["average_rating"]

    #print(res.json())
    return jsonify(apiRes)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/api/search")
def apiSearch():
    # Get form information.
    textSearch = request.values.get("textSearch")
    searchParam = request.args.get("searchFieldSelector")
    textSearch = "%"+textSearch+"%"
    if searchParam == 'ISBN':
        book = db.execute("SELECT * FROM books WHERE isbn ilike :isbn", {"isbn": textSearch}).fetchall()
    elif searchParam == 'TI':
        book = db.execute("SELECT * FROM books WHERE title ilike :title", {"title": textSearch}).fetchall()
    elif searchParam == 'AU':
        book = db.execute("SELECT * FROM books WHERE author ilike :author", {"author": textSearch}).fetchall()
    if not book:
        return jsonify('Unable to find any books.')

    apiRes = []
    i = 0
    while i < len(book):
        apiDict = {}
        apiDict["id"] = book[i]['id']
        apiDict["title"] = book[i]['title']
        apiDict["author"] = book[i]["author"]
        apiDict["year"] = book[i]["year"]
        apiDict["isbn"]  = book[i]['isbn']
        apiRes.append(dict(apiDict))
        i += 1

    return jsonify(apiRes)

@app.route("/profile")
def profile():
    if session.get('user_id') is None:
        return redirect("/login")
    else:
        user_id = session.get('user_id')
        user = db.execute("SELECT * FROM usertable WHERE id = :id", {"id": user_id}).fetchone();
        userReviews = db.execute("SELECT * FROM reviews JOIN books on books.id = book_id WHERE user_id = :user_id ", {"user_id": user_id}).fetchall();
        return render_template("profile.html", user=user, userReviews=userReviews)

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get('user_id') is None:
        return render_template("login.html")
    else:
        return redirect("profile")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/create_session", methods=["POST"])
def create_session():
    username = request.form.get("username")
    password = request.form.get("password")
    user = db.execute("SELECT * FROM usertable WHERE username = :username AND password = :password", {"username": username, "password": password}).fetchone();
    if user is None:
        flash(Markup('<div class="alert alert-danger text-center">The credentials provided are incorrect.  Please try again or <a href="/join">register</a> for a new account.</div>'))
        return redirect("/login")
    session["user_id"] = user["id"]
    return redirect("profile")

@app.route("/join")
def join():
    return render_template("join.html")

@app.route("/create", methods=["POST"])
def create():
    # Get form information.
    username = request.form.get("username")
    password = request.form.get("password")


    if db.execute("SELECT * FROM usertable WHERE username = :username", {"username": username}).rowcount == 1:
        flash(Markup('<div class="alert alert-danger text-center">That username already exists. Please try a different username</div>'))
        return redirect("join")
    db.execute("INSERT INTO usertable (username, password) VALUES (:username, :password)",
            {"username": username, "password": password})
    db.commit()

    user = db.execute("SELECT * FROM usertable WHERE username = :username", {"username": username}).fetchone();
    session["user_id"] = user["id"]
    return render_template("search.html")

@app.route("/submit_review", methods=["POST"])
def submit_review():
    review = request.form.get("review")
    rating = request.form.get("rating")
    book_id = request.form.get("book_id")
    user_id = request.form.get("user_id")
    if session.get('user_id') is None:
        flash(Markup('<div class="alert alert-danger text-center">You must be logged in to submit a review!</div>'))
        return redirect("login")
    else:
        if db.execute("SELECT * FROM reviews WHERE book_id = :book_id and user_id = :user_id", {"book_id": book_id, "user_id": user_id}).rowcount == 1:
            flash(Markup('<div class="alert alert-danger text-center">You have already reviewd this book</div>'))
            return redirect("join")
    db.execute("INSERT INTO reviews (user_id, book_id, review, rating) VALUES (:user_id, :book_id, :review, :rating)",
            {"user_id": user_id, "book_id": book_id, "review": review, "rating": rating})
    db.commit()
    return redirect("profile")