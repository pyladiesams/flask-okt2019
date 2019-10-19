from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
	username="",
	password="",
	hostname="",
	databasename=""
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Item(db.Model):
	__tablename__ = "items"
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(4096))

@app.route("/", methods = ["GET", "POST"])
def index():
	if request.method == "GET":
		return render_template("main_page.html", items = Item.query.all())
	else:
	    item = Item(name=request.form["item"])
	    db.session.add(item)
	    db.session.commit()
	return redirect(url_for('index'))

@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("item")
    item = Item.query.filter_by(name=name).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))






