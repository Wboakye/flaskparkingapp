from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone
        }

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.String(80), db.ForeignKey('Person.id'), unique=False, nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=False)



    def __repr__(self):
        return '<Cart %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "person_id": self.person_id,
            "address": self.address }