from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from instance.config import DB_URL

app = Flask(__name__,  template_folder='../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Instrument(db.Model):
    __tablename__ = "instrument"
    #id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), primary_key=True, unique=True)
    name = db.Column(db.String(200), unique=True)
    refreshed_at = db.Column(db.DateTime())
    from_date = db.Column(db.DateTime())
    to_date = db.Column(db.DateTime())
    exchange = db.Column(db.String(50))
    #valid_from = db.Column(db.DateTime())
    #valid_to = db.Column(db.DateTime())

    def __init__(self, code, name, refreshed_at, from_date, to_date, exchange):
        self.code = code
        self.name = name
        self.refreshed_at = refreshed_at
        self.from_date = from_date
        self.to_date = to_date
        self.exchange = exchange

    def __repr__(self):
        return '<Instrument %r>' % self.code


if __name__ == "__main__":
    db.create_all()
    db.session.commit()


