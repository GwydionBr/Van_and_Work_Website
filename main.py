from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from flask_bootstrap import Bootstrap5

from forms import CreatePostForm


app = Flask(__name__)
bootstrap = Bootstrap5(app)

app.secret_key = "some secret string"

class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spots.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Spots(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    adresse: Mapped[str] = mapped_column(String(250), nullable=False)
    date_start: Mapped[str] = mapped_column(String(250), nullable=False)
    date_end: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[str] =mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    internet_rating: Mapped[str] = mapped_column(Integer, nullable=False)
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
    return render_template("learn-more.html", title="Learn more")

@app.route("/delete/<int:spot_id>")
def delete_post(spot_id):
    spot_to_delete = db.get_or_404(Spots, spot_id)
    db.session.delete(spot_to_delete)
    db.session.commit()
    return redirect(url_for('spots'))

@app.route("/add_post", methods=["GET", "POST"])
def add_spot():
    add_spot_form = CreatePostForm()
    if add_spot_form.validate_on_submit():
        new_spot = Spots(title=add_spot_form.title.data,
                         adresse=add_spot_form.location.data,
                         date_start=str(add_spot_form.date_start.data),
                         date_end=str(add_spot_form.date_end.data),
                         rating=add_spot_form.rating.data,
                         description=add_spot_form.description.data,
                         internet_rating=add_spot_form.internet_rating.data,
                         standort=add_spot_form.location.data,
                         )
        db.session.add(new_spot)
        db.session.commit()
        return redirect(url_for('spots'))
    return render_template("add_spot.html", title="Add Spot", form=add_spot_form)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
