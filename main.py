from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date


app = Flask(__name__)

class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spots.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Spots(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    adresse: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[int] =mapped_column(Integer, nullable=False)
    internet_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    standort: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html", title="Home")

@app.route("/spots")
def spots():
    spots = db.session.execute(db.select(Spots)).scalars().all()

    return render_template("spots.html", title="Spots", all_spots=spots)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")

@app.route("/learn_more")
def learn_more():
    return render_template("learn-more.html", title="Learn_more")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
