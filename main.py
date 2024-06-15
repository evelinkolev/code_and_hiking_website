from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import random

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chalets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Chalet(db.Model):
    __tablename__ = 'chalets'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    map_url: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    rating: Mapped[float] = mapped_column(DECIMAL(3, 2), nullable=False)
    night_price_bgn: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# Ensure database creation within an application context
with app.app_context():
    db.create_all()
    # chalets = Chalet.query.all()
    # print(chalets)

@app.route("/")
def home():
    chalets = Chalet.query.all()
    return render_template("index.html", chalets=chalets)


@app.route("/add", methods=["GET", "POST"])
def post_new_chalet():
    if request.method == "POST":
        new_chalet = Chalet(
            name=request.form.get("name"),
            location=request.form.get("location"),
            map_url=request.form.get("map_url"),
            image_url=request.form.get("image_url"),
            has_wifi=request.form.get("has_wifi") == 'on',
            rating=request.form.get("rating"),
            night_price_bgn=request.form.get("night_price_bgn"),
        )
        db.session.add(new_chalet)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/update-chalet/<int:chalet_id>", methods=["GET", "POST"])
def update_chalet(chalet_id):
    chalet = Chalet.query.get_or_404(chalet_id)
    if request.method == "POST":
        chalet.name = request.form.get("name")
        chalet.location = request.form.get("location")
        chalet.map_url = request.form.get("map_url")
        chalet.image_url = request.form.get("image_url")
        chalet.has_wifi = 'has_wifi' in request.form
        chalet.rating = float(request.form.get("rating"))
        chalet.night_price_bgn = float(request.form.get("night_price_bgn"))
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("update.html", chalet=chalet)




if __name__ == '__main__':
    app.run(debug=True)
