from __future__ import annotations

from typing import List

from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db

UserInterests = Table(
    "users_interests",
    db.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("interest_id", ForeignKey("interests.id")),
)

UserEvents = Table(
    "users_events",
    db.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("event_id", ForeignKey("events.id")),
)

OrganizerEvents = Table(
    "organizers_events",
    db.metadata,
    Column("organizer_id", ForeignKey("organizers.id")),
    Column("event_id", ForeignKey("events.id")),
)

OrganizerInterests = Table(
    "organizers_interests",
    db.metadata,
    Column("organizer_id", ForeignKey("organizers.id")),
    Column("interest_id", ForeignKey("interests.id")),
)

EventInterests = Table(
    "events_interests",
    db.metadata,
    Column("event_id", ForeignKey("events.id")),
    Column("interest_id", ForeignKey("interests.id")),
)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    role = "user"
    name = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    faculty = db.Column(db.String(255))
    major = db.Column(db.String(255))
    campus = db.Column(db.String(255))
    year_of_study = db.Column(db.String(255))
    events: Mapped[List[Event]] = relationship(secondary=UserEvents, back_populates="users")
    interests: Mapped[List[Interest]] = relationship(
        secondary=UserInterests, back_populates="users"
    )

    def add_interest(self, interest):
        if interest not in self.interests:
            self.interests.append(interest)

    def add_event(self, event):
        if event not in self.events:
            self.events.append(event)

    def __repr__(self):
        return "<User %r" % self.name

class Interest(db.Model):
    __tablename__ = "interests"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    events: Mapped[List[Event]] = relationship(secondary=EventInterests, back_populates="interests")
    users: Mapped[List[User]] = relationship(secondary=UserInterests, back_populates="interests")
    organizers: Mapped[List[Organizer]] = relationship(
        secondary=OrganizerInterests, back_populates="interests"
    )

    def __repr__(self):
        return f"Interest: {self.name}"


class Organizer(UserMixin, db.Model):
    __tablename__ = "organizers"
    id = db.Column(db.Integer, primary_key=True)
    role = "organizer"
    organizer_name: Mapped[str] = mapped_column(String(30), nullable=False)
    organizer_email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(10000), nullable=True)
    image_link: Mapped[str] = mapped_column(String(1000), nullable=True)
    campus: Mapped[str] = mapped_column(String(5), nullable=True)
    website: Mapped[str] = mapped_column(String(30), nullable=True)
    instagram: Mapped[str] = mapped_column(String(30), nullable=True)
    linkedin: Mapped[str] = mapped_column(String(30), nullable=True)
    events: Mapped[List[Event]] = relationship(
        secondary=OrganizerEvents, back_populates="organizers"
    )
    interests: Mapped[List[Interest]] = relationship(
        secondary=OrganizerInterests, back_populates="organizers"
    )

    def add_interest(self, interest):
        if interest not in self.interests:
            self.interests.append(interest)

    def add_event(self, event):
        if event not in self.events:
            self.events.append(event)

    def __repr__(self):
        return "<Organizer %r" % self.organizer_email


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    event_name: Mapped[str] = mapped_column(String(100), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey("organizers.id"), nullable=True)
    description: Mapped[str] = mapped_column(String(10000), nullable=True)
    image_link: Mapped[str] = mapped_column(String(1000), nullable=True)
    date: Mapped[str] = mapped_column(String(100), nullable=False)
    time: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    google_map_link: Mapped[str] = mapped_column(String(100), nullable=False)
    fee: Mapped[int] = mapped_column(Integer, nullable=True)
    has_rsvp: Mapped[str] = mapped_column(String(100), nullable=False)
    external_registration_link: Mapped[str] = mapped_column(String(200), nullable=True)
    users: Mapped[List[User]] = relationship(secondary=UserEvents, back_populates="events")
    organizers: Mapped[List[Organizer]] = relationship(
        secondary=OrganizerEvents, back_populates="events"
    )
    interests: Mapped[List[Interest]] = relationship(
        secondary=EventInterests, back_populates="events"
    )

    def add_user(self, interest):
        if interest not in self.interests:
            self.interests.append(interest)
    def add_interest(self, interest):
        if interest not in self.interests:
            self.interests.append(interest)
    def add_organizer(self, event):
        if event not in self.events:
            self.events.append(event)

    def __repr__(self):
        return f"Event: {self.event_name}"
