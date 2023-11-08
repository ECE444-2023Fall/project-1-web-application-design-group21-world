from flask_login import LoginManager, UserMixin
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    faculty = db.Column(db.String(255))
    major = db.Column(db.String(255))
    campus = db.Column(db.String(255))
    yearOfStudy = db.Column(db.String(255))

    def __repr__(self):
        return "<User %r" % self.name

    # interest = db.relationship("Interest", db.ForeignKey('interests.id'), )


class Interest(db.Model):
    __tablename__ = "interests"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return f"Interest: {self.name}"


class OrganizerInterest(db.Model):
    __tablename__ = "organizer_interests"
    organizer_id = db.Column(db.Integer, db.ForeignKey("organizers.id"), primary_key=True)
    interest_id = db.Column(db.Integer, db.ForeignKey("interests.id"), primary_key=True)


class Organizer(UserMixin,db.Model):
    __tablename__ = "organizers"
    id = db.Column(db.Integer, primary_key=True)
    organizer_name: Mapped[str] = mapped_column(String(30), nullable=False)
    organizer_email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(10000), nullable=True)
    campus: Mapped[str] = mapped_column(String(5), nullable=True)
    website: Mapped[str] = mapped_column(String(30), nullable=True)
    instagram: Mapped[str] = mapped_column(String(30), nullable=True)
    linkedin: Mapped[str] = mapped_column(String(30), nullable=True)

    def __repr__(self):
        return "<Organizer %r" % self.organizer_email

    # Define a relationship with Interests, assuming you have a Many-to-Many relationship
    # interests = db.relationship("Interest", secondary="organizer_interests", backref="organizers")


class EventInterest(db.Model):
    __tablename__ = "event_interests"
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), primary_key=True)
    interest_id = db.Column(db.Integer, db.ForeignKey("interests.id"), primary_key=True)

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    event_name: Mapped[str] = mapped_column(String(100), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizers.id"), nullable=True)
    description: Mapped[str] = mapped_column(String(10000), nullable=True)
    date: Mapped[str] = mapped_column(String(100), nullable=False)
    time: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    google_map_link: Mapped[str] = mapped_column (String(100), nullable=False)
    fee: Mapped[int] = mapped_column(Integer, nullable=True)
    #interest_area: Mapped[str] = mapped_column(String, nullable=False)
    has_rsvp: Mapped[str] = mapped_column(String(100), nullable=False)
    external_registration_link: Mapped[str] = mapped_column(String(200), nullable=True)