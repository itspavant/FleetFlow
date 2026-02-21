from app.extensions import db
from app.models.base import BaseModel


class FuelLog(BaseModel):
    __tablename__ = "fuel_logs"

    trip_id = db.Column(
        db.Integer,
        db.ForeignKey("trips.id"),
        nullable=False
    )

    liters = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    trip = db.relationship("Trip", backref="fuel_logs")