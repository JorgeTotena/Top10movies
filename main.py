from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
# initialize the app with the extension
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)
Bootstrap(app)

class Movie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True)
    year: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)
    ranking: Mapped[int] = mapped_column(nullable=False)
    review: Mapped[int] = mapped_column(nullable=False)
    img_url: Mapped[str] = mapped_column(unique=True, nullable=False)

class EditForm(FlaskForm):
    new_rating = StringField(label="Your rating out of 10 e.g 7.3", validators=[DataRequired()])
    new_review = StringField(label="Your review", validators=[DataRequired()])
    edit_rating = SubmitField(label="Done")

# CREATE DB

# with app.app_context():
#     db.create_all()


# ADD DATA

# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")

# second_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )
#
# with app.app_context():
#     db.session.add(new_movie)
#     db.session.commit()


@app.route("/")
def home():
    movies = db.session.execute(db.select(Movie).order_by(desc(Movie.rating))).scalars().all()
    print(movies)
    return render_template("index.html", movies=movies)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    form = EditForm()
    movies = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
    if form.validate_on_submit():
        movies.rating = float(form.new_rating.data)
        movies.review = form.new_review.data
        # movie_id = request.args.get("id") OTHER WAY TO DO IT
        # movie = db.get_or_404(Movie, movie_id)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('edit.html', movies=movies, form=form)

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    movies_to_delete = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
    db.session.delete(movies_to_delete)
    db.session.commit()
    return redirect(url_for("home"))
    return render_template('delete.html', movies=movies_to_delete)


if __name__ == '__main__':
    app.run(debug=True)
