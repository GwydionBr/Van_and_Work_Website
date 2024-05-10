from flask import Flask, render_template, redirect, url_for, abort, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap5
from forms import CreatePostForm, AdminForm
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


app = Flask(__name__)
bootstrap = Bootstrap5(app)

app.secret_key = "some secret string"

login_manager = LoginManager()
login_manager.init_app(app)


class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spots.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(1000))

class Spots(db.Model):
    __tablename__ = "spots"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    date_start: Mapped[datetime.date] = mapped_column(DateTime(), nullable=False)
    date_end: Mapped[datetime.date] = mapped_column(DateTime(), nullable=False)
    rating: Mapped[str] =mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    internet_rating: Mapped[str] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()


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

@app.route("/login", methods=["GET", "POST"])
def admin_login():
    admin_form = AdminForm()
    if admin_form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == admin_form.email.data)).scalar()
        if not user:
            flash('Thats not the valid Email!')
            return redirect(url_for('admin_login'))
        if not check_password_hash(user.password, admin_form.password.data):
            flash('Password is not correct! Please try again.')
            return redirect(url_for('admin_login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
        return redirect(url_for("home"))
    return render_template("admin.html", title="Admin", form=admin_form)


@app.route("/logout")
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/add_spot", methods=["GET", "POST"])
@login_required
def add_spot():
    add_spot_form = CreatePostForm()
    if add_spot_form.validate_on_submit():
        print(type(add_spot_form.date_end.data))
        new_spot = Spots(title=add_spot_form.title.data,
                         date_start=add_spot_form.date_start.data,
                         date_end=add_spot_form.date_end.data,
                         rating=add_spot_form.rating.data,
                         description=add_spot_form.description.data,
                         internet_rating=add_spot_form.internet_rating.data,
                         location=add_spot_form.location.data,
                         )
        db.session.add(new_spot)
        db.session.commit()
        return redirect(url_for('spots'))
    return render_template("add_spot.html", title="Add Spot", form=add_spot_form)

@app.route("/edit_spot/<int:spot_id>", methods=["GET", "POST"])
@login_required
def edit_spot(spot_id):
    spot_to_edit = db.get_or_404(Spots, spot_id)
    edit_form = CreatePostForm(
        title=spot_to_edit.title,
        date_start=spot_to_edit.date_start,
        date_end=spot_to_edit.date_end,
        rating=spot_to_edit.rating,
        description=spot_to_edit.description,
        internet_rating=spot_to_edit.internet_rating,
        location=spot_to_edit.location,
    )
    if edit_form.validate_on_submit():
        spot_to_edit.title=edit_form.title.data
        spot_to_edit.date_start=edit_form.date_start.data
        spot_to_edit.date_end=edit_form.date_end.data
        spot_to_edit.rating=edit_form.rating.data
        spot_to_edit.description=edit_form.description.data
        spot_to_edit.internet_rating=edit_form.internet_rating.data
        spot_to_edit.location=edit_form.location.data
        db.session.commit()
        return redirect(url_for('spots'))
    return render_template("add_spot.html", title="Edit Spot", form=edit_form)

@app.route("/delete/<int:spot_id>")
@login_required
def delete_post(spot_id):
    spot_to_delete = db.get_or_404(Spots, spot_id)
    db.session.delete(spot_to_delete)
    db.session.commit()
    return redirect(url_for('spots'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
