# Importing the flask lib , the render template to get the pages to run from a server , request for the HTTP requests to the server
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func


# initialisation of the app
app = Flask(__name__)

# config the connection of the database with postgresql
# app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres123@localhost/height_collector'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://hgprcgcsnqwfmd:61beaef20b378bd07c1e9d496ab055cd1afe36cc6e49d549547896265c616eb7@ec2-54-81-37-115.compute-1.amazonaws.com:5432/d3e5qf32h78m86?sslmode=require'

# create an object "db" with SQLAlchemy
db = SQLAlchemy(app)

# Class template for the table


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)
    height_ = db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_

# decorator
@app.route("/")
# method for showing home page
def index():
    return render_template("index.html")

# use of POST method ....we need to specify that as GET method is the default
@app.route("/success", methods=['POST'])
def success():
    # extracting the name attribute of the inputs
    if request.method == 'POST':
        email = request.form["email_name"]
        height = request.form["height_name"]
        if(db.session.query(Data).filter(Data.email_ == email).count() == 0):
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height_)).scalar()
            average_height = round(average_height, 1)
            count = db.session.query(Data.height_).count()
            send_email(email, height, average_height, count)
            return render_template('success.html')
    return render_template('index.html', text="seems like we've got the data from that email address already!")


# app starts from here
if __name__ == '__main__':
    app.debug = True
    app.run()
