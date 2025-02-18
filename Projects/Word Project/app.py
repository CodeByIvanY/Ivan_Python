import os
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finalproject.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return render_template("index.html")


@app.route("/addword", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("addword.html" )
    else:
        word = request.form.get("word")
        speech = request.form.get("speech")
        definition = request.form.get("definition")
        user_id = session["user_id"]
        date = datetime.datetime.now()
        db.execute("INSERT INTO vocabulary (user_id, word, speech, definition, date) VALUES (?, ?, ?, ?, ?)", user_id, word, speech, definition, date)
        flash(f"Vocabulary [{word}] is created, please review!")
        return redirect("/")


@app.route("/vocabularies")
@login_required
def vocabularies():
    user_id = session["user_id"]
    vocabularies_db = db.execute(
        "SELECT * FROM vocabulary WHERE user_id = ?", user_id
    )
    return render_template("vocabularies.html", vocabularies=vocabularies_db)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/updateword", methods=["GET", "POST"])
@login_required
def update():
    """remove word"""
    if request.method == "GET":
        user_id = session["user_id"]
        words_user = db.execute(
            "SELECT * FROM vocabulary WHERE user_id = ?", user_id)
        return render_template(
            "updateword.html", words=[row["word"] for row in words_user], wordsdb = words_user
        )
    else:
        word_id_bf = request.form.get("id")
        word_id_bf_s2 = word_id_bf.find(":")
        word_id = word_id_bf[:word_id_bf_s2]
        user_id = session["user_id"]

        if not request.form.get("updatedword"):
            updated_word = db.execute("SELECT word FROM vocabulary WHERE user_id = ? AND id = ?", user_id, word_id)[0]["word"]
        else:
            updated_word = request.form.get("updatedword").strip()

        if not request.form.get("updatedspeech"):
            updated_speech = db.execute("SELECT speech FROM vocabulary WHERE user_id = ? AND id = ?", user_id, word_id)[0]["speech"]
        else:
            updated_speech = request.form.get("updatedspeech").strip()

        if not request.form.get("updateddefinition"):
            updated_definition = db.execute("SELECT definition FROM vocabulary WHERE user_id = ? AND id = ?", user_id, word_id)[0]["definition"]
        else:
            updated_definition = request.form.get("updateddefinition").strip()

        date = datetime.datetime.now()

        db.execute("UPDATE vocabulary SET word = ?, speech = ?, definition = ?, date = ? WHERE user_id = ? AND id = ?", updated_word, updated_speech, updated_definition, date, user_id, word_id)
        flash("Updated!")

        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Require that a user input a username, implemented as a text field whose name is username. Render an apology if the user’s input is blank or the username already exists.
        if not username:
            return apology("Must Input Username")

        if not password:
            return apology("Must Input Password")

        # Require that a user input a password, implemented as a text field whose name is password, and then that same password again, implemented as a text field whose name is confirmation. Render an apology if either input is blank or the passwords do not match.
        if not confirmation:
            return apology("Must Input Confirmation")

        if password != confirmation:
            return apology("Password Do Not Match")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash
            )
        except:
            return apology("Username already exists")
        session["user_id"] = new_user

        return redirect("/")


@app.route("/removeword", methods=["GET", "POST"])
@login_required
def remove():
    """remove word"""
    if request.method == "GET":
        user_id = session["user_id"]
        words_user = db.execute(
            "SELECT * FROM vocabulary WHERE user_id = ?", user_id)
        return render_template(
            "removeword.html", words=[row["word"] for row in words_user], wordsdb = words_user
        )
    else:
        user_id = session["user_id"]
        word_id_bf = request.form.get("id")
        word_id_bf_s2 = word_id_bf.find(":")
        word_id = word_id_bf[:word_id_bf_s2]
        removed_word = db.execute("SELECT word FROM vocabulary WHERE user_id = ? AND id = ?", user_id, word_id)[0]["word"]
        db.execute("DELETE FROM vocabulary WHERE user_id = ? AND id = ?", user_id, word_id)
        flash(f"[{removed_word}] is removed, please review!")

        return redirect("/")

@app.route("/remove", methods=["POST"])
@login_required
def remove2():
    """remove word"""
    id = request.form.get("id")
    if id:
        db.execute ("DELETE FROM vocabulary WHERE id = ?", id)
    flash("Removed!")

    return redirect ("/")
    flash(f"Vocabulary [{word}] is created, please review!")

@app.route("/P01WordTest", methods=["GET", "POST"])
@login_required
def WordTest():
    """Word Test"""
    if request.method == "GET":
        user_id = session["user_id"]
        # SELECT id, word FROM vocabulary WHERE user_id = 1 order by RANDOM()  LIMIT 10;
        vocabularies_db = db.execute("SELECT id, word FROM vocabulary WHERE user_id = ? ORDER BY RANDOM() LIMIT 10", user_id)

        return render_template("P01WordTest.html", vocabularies=vocabularies_db)
    else:
        word_0 = request.form.get("word_0")
        word_1 = request.form.get("word_1")
        word_2 = request.form.get("word_2")
        word_3 = request.form.get("word_3")
        word_4 = request.form.get("word_4")
        word_5 = request.form.get("word_5")
        word_6 = request.form.get("word_6")
        word_7 = request.form.get("word_7")
        word_8 = request.form.get("word_8")
        word_9 = request.form.get("word_9")
        id_0 = request.form.get("id_0")
        id_1 = request.form.get("id_1")
        id_2 = request.form.get("id_2")
        id_3 = request.form.get("id_3")
        id_4 = request.form.get("id_4")
        id_5 = request.form.get("id_5")
        id_6 = request.form.get("id_6")
        id_7 = request.form.get("id_7")
        id_8 = request.form.get("id_8")
        id_9 = request.form.get("id_9")
        x=0
        match_0 = db.execute("SELECT word FROM vocabulary WHERE id = ?", id_0)[0]["word"].upper()
        if word_0.upper().strip() == match_0:
            x += 1

        match_1 = db.execute("SELECT word FROM vocabulary WHERE id = ?", id_1)[0]["word"].upper()
        if word_1.upper().strip()  == match_1:
            x += 1

        match_2 = db.execute("SELECT word FROM vocabulary WHERE id = ?", id_2)[0]["word"].upper()
        if word_2.upper().strip()  == match_2:
            x += 1

        match_3 = db.execute("SELECT word FROM vocabulary WHERE id = ?", id_3)[0]["word"].upper()
        if word_3.upper().strip()  == match_3:
            x += 1

        match_4 = db.execute("SELECT word FROM vocabulary WHERE id = ?", id_4)[0]["word"].upper()
        if word_4.upper().strip()  == match_4:
            x += 1

        match_5 = db.execute("SELECT word FROM vocabulary WHERE id = ?", id_5)[0]["word"].upper()
        if word_5.upper().strip()  == match_5:
            x += 1

        match_6 = db.execute("SELECT word FROM vocabulary WHERE id = ?", id_6)[0]["word"].upper()
        if word_6.upper().strip()  == match_6:
            x += 1

        match_7 = db.execute("SELECT word FROM vocabulary WHERE id = ?", id_7)[0]["word"].upper()
        if word_7.upper().strip()  == match_7:
            x += 1

        match_8 = db.execute("SELECT word FROM vocabulary WHERE id = ?", id_8)[0]["word"].upper()
        if word_8.upper().strip()  == match_8:
            x += 1

        match_9 = db.execute("SELECT word FROM vocabulary WHERE id = ?", id_9)[0]["word"].upper()
        if word_9.upper().strip()  == match_9:
            x += 1

        flash(f" You got {x} out of 10 correct in your responses. ")
        return redirect("P01WordTest")


@app.route("/P02WordGuess", methods=["GET"])
@login_required
def WordGuess():
    if request.method == "GET":
        user_id = session["user_id"]
        # SELECT id, word FROM vocabulary WHERE user_id = 1 order by RANDOM()  LIMIT 10;
        vocabulary = db.execute("SELECT id, word FROM vocabulary WHERE user_id = ? ORDER BY RANDOM() LIMIT 1", user_id)[0]["word"].upper()

        return render_template("P02WordGuess.html", vocabulary=vocabulary)
    else:
        return render_template("P02WordGuess.html")
