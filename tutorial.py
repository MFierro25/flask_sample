from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#  used to sign session cookies for protection against cookie data tampering
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# stores permanent session data
app.permanent_session_lifetime = timedelta(days=15)


# database object
db = SQLAlchemy(app)
#  create model


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    
    #take variables to create a new object
    def __init__(self, name, email):
        self.name = name
        self.email = email

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
        
        # find all users in table with that name, first entry
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
            
        # create user and add to db    
        else:
            usr = users(user, "")
            db.session.add(usr)
            # dont forget to commit changes to save
            db.session.commit()
            
        flash("You succesfully logged in!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged in!")
            return redirect(url_for("user"))       
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            # change and save users email
            found_user.email = email
            db.session.commit()
            
            flash("Email was saved")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash("Please login")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        session.pop("user", None)
        session.pop("email", None)
    # flashes a message
    flash(f"You have been logged out, {user}", "info")
    return redirect(url_for("login"))

@app.route("/view")
def view():
    # return all users in database
    return render_template("view.html", values=users.query.all())   

if __name__ == "__main__":
    # created database
    db.create_all()
    app.run(debug=True)