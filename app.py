from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "canilive"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def cupcake_home():
    """display the cupcake homepage"""

    return render_template("index.html")

@app.route("/api/cupcakes")
def show_cupcakes():
    """Get all cupcakes in db"""
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = cupcakes)

@app.route("/api/cupcakes/<int:id>")
def show_cupcake(id):
    """Get info for a specific cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake = cupcake.serialize())

@app.route("/api/cupcakes", methods=["POST"])
def add_cupcake():
    """Add a new cupcake to the db"""

    data = request.json

    cupcake = Cupcake(
        flavor = data["flavor"],
        rating = data["rating"],
        size = data["size"],
        image = data["image"] or None)

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 201)


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """Change a cupcake to the db"""

    data = request.json

    cupcake = Cupcake.query.get_or_404(id)
    
    cupcake.flavor = data["flavor"]
    cupcake.rating = data["rating"]
    cupcake.size = data["size"]
    cupcake.image = data["image"]

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    """Delete a cupcake from the db"""

    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")