#encoding: utf-8

from exits import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100), nullable=False)



class Car_rental(db.Model):
    __tablename__ = 'car_rental'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))

    author = db.relationship('User',backref =db.backref('car_rental'))


class Cars(db.Model):
    __tablename__ = 'Cars'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    carname=db.Column(db.Text,nullable=True)
    Bdatetime=db.Column(db.Text,nullable=True)
    Bday = db.Column(db.Text, nullable=True)
    Btime = db.Column(db.Text, nullable=True)
    Rdatetime = db.Column(db.Text, nullable=True)
    Rday = db.Column(db.Text, nullable=True)
    Rtime = db.Column(db.Text, nullable=True)
    carprice=db.Column(db.Integer,nullable=True)
    Location = db.Column(db.Text, nullable=True)


    create_time = db.Column(db.DateTime,default=datetime.now)
    cattype=db.Column(db.String(100),nullable=True)
    gearbox=db.Column(db.String(100),nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('Cars'))



class CarsDataset(db.Model):
    __tablename__ = 'CarsDataset'

    name=db.Column(db.Text,nullable=True)
    price=db.Column(db.Integer,nullable=True)
    vehicleType = db.Column(db.Text, nullable=True)
    yearOfRegistration = db.Column(db.Integer, nullable=True)
    gearbox = db.Column(db.Text, nullable=True)
    kilometer = db.Column(db.Integer, nullable=True)
    brand= db.Column(db.Text, nullable=True)
    lng=db.Column(db.FLOAT,nullable=True)
    lat=db.Column(db.FLOAT,nullable=True)
    seat = db.Column(db.Integer, nullable=True)
    bluetooth = db.Column(db.Text, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    # create_time = db.Column(db.DateTime,default=datetime.now)

    author = db.relationship('User', backref=db.backref('CarsDataset'))

    def serializer(self):
        """
        序列化
        :return: dict
        """
        json = {
            'lng': self.lng,
            'lat': self.lat,
            'name': self.name,
            'price': self.price,
            'vehicleType': self.vehicleType,
            'brand': self.brand,
            'yearOfRegistration': self.yearOfRegistration,
            'seat': self.seat,
            'bluetooth': self.bluetooth,
            'kilometer': self.kilometer,



        }
        return json






