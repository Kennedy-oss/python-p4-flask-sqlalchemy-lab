from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Zookeeper(db.Model):
    __tablename__ = 'zookeeper'  # Explicitly define the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    animals = db.relationship('Animal', backref='zookeeper', lazy=True)

class Animal(db.Model):
    __tablename__ = 'animals'  # Explicitly define the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    species = db.Column(db.String(128), nullable=False)
    zookeeper_id = db.Column(db.Integer, db.ForeignKey('zookeeper.id'), nullable=False)  # Ensure this matches the table name
    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosure.id'), nullable=False)

class Enclosure(db.Model):
    __tablename__ = 'enclosure'  # Explicitly define the table name
    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String(128), nullable=False)
    open_to_visitors = db.Column(db.Boolean, default=True, nullable=False)
    animals = db.relationship('Animal', backref='enclosure', lazy=True)

