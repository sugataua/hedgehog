MODE_BUS = 0
MODE_TRAIN = 1

TYPE_STOP = 0
TYPE_STATION = 1


from hedgehog import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)    
    email = db.Column(db.String(254), unique=True)
    pwd_hash = db.Column(db.String(256))
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.pwd_hash, password)
    
    def __repr__(self):
        return '<User %r>' % self.username
    

class Locality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50))
    visit_counter = db.Column(db.Integer, default=0)
    region = db.Column(db.String(200))  # Область
    district = db.Column(db.String(200))  # Район
    locality_type = db.Column(db.String(50), default='н.п.')
    coordinate_lat = db.Column(db.Float)
    coordinate_lon = db.Column(db.Float)
    
    deleted = db.Column(db.Boolean, default=False)
        
    stations = db.relationship('Station', backref='locality',
                                lazy='dynamic')
    """
    def __init__(self, name):
        self.name = name
    """


    def __init__(self, name = None, locality_type = None, region = None, district = None, lat = None, lon = None):
        self.name = name
        self.locality_type = locality_type
        self.district = district
        self.region = region
        self.coordinate_lat = float(lat)
        self.coordinate_lon = float(lon)

        
    def __repr__(self):
        return '<Locality %r>' % self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        self.deleted = True
        for station in self.stations:
            station.delete()
        db.session.commit()

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(256), default="зупинка")
    transport_mode = db.Column(db.SmallInteger, default=MODE_BUS)    
    station_type = db.Column(db.SmallInteger, default=TYPE_STOP)
    
    coordinate_lat = db.Column(db.Float)
    coordinate_lon = db.Column(db.Float)

    phone_number = db.Column(db.String(32)) 
    address = db.Column(db.String(256))    
    luggage_storage = db.Column(db.Boolean)
    toilet = db.Column(db.Boolean)
    ticket_office = db.Column(db.Boolean)
    
    deleted = db.Column(db.Boolean, default=False)
        
    locality_id = db.Column(db.Integer, db.ForeignKey('locality.id'))    
    photo_timetables = db.relationship('PhotoTimetable', backref="on_station", lazy='dynamic')

    
    def __init__(self, name, locality_id):
        self.name = name
        self.locality_id = locality_id

    def __repr__(self):
        return '<Station %r>' % self.name

    def delete(self):
        self.deleted = True
        for pt in self.photo_timetables:
            pt.delete()
        db.session.commit()
        
        
class PhotoTimetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station = db.Column(db.Integer, db.ForeignKey('station.id'))    
    url_img_link = db.Column(db.String(256))
    author_comment = db.Column(db.Text)
        
    deleted = db.Column(db.Boolean, default=False)
    
    def __init__(self, station, url_img_link):        
        self.station = station
        self.url_img_link = url_img_link
        
    def __init__(self, station, url_img_link, comment):        
        self.station = station
        self.url_img_link = url_img_link
        self.author_comment = comment

    def __repr__(self):
        return '<PhotoTimetable link %r>' % self.url_img_link

    def delete(self):
        self.deleted = True
        db.session.commit()
    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    
    
