from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
#app.config['SQLALCHEMY_DATABASE_URI'] =
DB_URL = 'postgresql://localhost/wikidb'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning


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

    def __init__(self, code, name, refreshed_at, from_date, to_date, exchange):
        self.code = code
        self.name = name
        self.refreshed_at = refreshed_at
        self.from_date = from_date
        self.to_date = to_date
        self.exchange = exchange


    def __repr__(self):
        return '<Instrument %r>' % self.code

'''
db.create_all()
db.session.commit()
'''