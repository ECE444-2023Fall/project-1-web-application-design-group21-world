from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return "<User %r" % self.username

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


class Organizer(db.Model):
    __tablename__ = "organizers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organizer_name: Mapped[str] = mapped_column(String(30), nullable=False)
    organizer_email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(10000), nullable=False)
    contact_email: Mapped[str] = mapped_column(String(30), nullable=False)
    website: Mapped[str] = mapped_column(String(30))
    instagram: Mapped[str] = mapped_column(String(30))
    linkedin: Mapped[str] = mapped_column(String(30))
    campus: Mapped[str] = mapped_column(String(3), nullable=False)

    # Define a relationship with Interests, assuming you have a Many-to-Many relationship
    interests = db.relationship("Interest", secondary="organizer_interests", backref="organizers")


class EventInterest(db.Model):
    __tablename__ = "event_interests"
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), primary_key=True)
    interest_id = db.Column(db.Integer, db.ForeignKey("interests.id"), primary_key=True)


class Event(db.Model):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizers.id"), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    google_map_link = db.Column(db.String(200))  # Optional
    fee = db.Column(db.Float)  # Optional
    has_rsvp = db.Column(db.Boolean, nullable=False)
    external_registration_link = db.Column(db.String(200), nullable=False)

    # interests = db.relationship("Interest", secondary="event_interests", back_populates="events")
