from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)
#  used to sign session cookies for protection against cookie data tampering
app.secret_key = "hello"
# stores permanent session data
app.permanent_session_lifetime = timedelta(days=15)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # sets specific session to permanent
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash("You succesfully logged in!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged in!")
            return redirect(url_for("user"))
        
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash("Please login")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        session.pop("user", None)
    # flashes a message
    flash(f"You have been logged out, {user}", "info")
    return redirect(url_for("login"))   

if __name__ == "__main__":
    app.run(debug=True)