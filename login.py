import flask
from flask import Flask,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://arnav:password@localhost/users'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = '123'
db = SQLAlchemy(app)
class Users(db.Model):
    name  = db.Column(db.String(120),primary_key=True)
    email = db.Column(db.String(80),unique=True)
    password  = db.Column(db.String(80),unique=True)

    def __init__(self,name,email,password,number):
        self.email = email
        self.name=name
        self.password = password


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route('/register',methods=["GET","POST"])
def register():
    global db,app
    form = request.form
    password = sha256_crypt.encrypt(form["password"])
    session['name'] = form['name']
    user= Users(form["name"],form["email"],password)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://arnav:password@localhost/{}'.format("users")
    db.session.add(user)
    db.session.commit()
    engine = create_engine("mysql://arnav:password@localhost/{}".format(form["clubNumber"]))
    if not database_exists(engine.url):
        create_database(engine.url)
#    db = SQLAlchemy(app)
    db.create_all()
    return ('registered')

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
