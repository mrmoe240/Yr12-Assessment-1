from flask import Flask, render_template, request, session, redirect
import db

app = Flask(__name__)
app.secret_key = "gtg"

@app.route("/")
def Home():
    guessData = db.GetAllGuesses()
    return render_template("index.html", guesses=guessData)

@app.route("/login", methods=["GET", "POST"])
def Login():


    if request.method == "POST":
        username = request.form['username'] 
        password = request.form['password']

        # Did they provide good details
        user = db.CheckLogin(username, password)
        if user:
            # Yes! Save their username then
            session['username'] = user['username']
            session['id'] = user['id']

            # Send them back to the homepage
            return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def Register():

    # If they click the submit button, let's register
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Try and add them to the DB
        if db.RegisterUser(username, password):
            # Success! Let's go to the homepage
            return redirect("/")
       
    return render_template("register.html")


@app.route("/add", methods=["GET","POST"])
def Add():

    # Check if they are logged in first
    if session.get('username') == None:
        return redirect("/")


    # Did they click submit?
    if request.method == "POST":
        user_id = session['id']
        date = request.form['date']
        game = request.form['game']
        score = request.form['score']
        review = request.form['review']

        # Send the data to add our new guess to the db
        db.AddGuess(user_id, date, game, score, review,)

    return render_template("add.html")

@app.route("/delete", methods=["GET","POST"])
def delete():

    user_id = session['id']
    date = request.form['date']
    game = request.form['game']
    score = request.form['score']
    review = request.form['review']
    db.delete(user_id, date, game, score, review)


app.run(debug=True, port=80)