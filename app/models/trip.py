from app.extensions import db
from app.models.base import BaseModel
from app.models.enums import TripStatus
from datetime import datetime

fuel_logs = db.relationship(
    "FuelLog",
    backref="trip",
    cascade="all, delete-orphan"
)

class Trip(BaseModel):
    __tablename__ = "trips"

    vehicle_id = db.Column(
        db.Integer,
        db.ForeignKey("vehicles.id"),
        nullable=False
    )

    driver_id = db.Column(
        db.Integer,
        db.ForeignKey("drivers.id"),
        nullable=False
    )

    cargo_weight = db.Column(db.Float, nullable=False)

    origin = db.Column(db.String(150), nullable=False)
    destination = db.Column(db.String(150), nullable=False)

    revenue = db.Column(db.Float, default=0)

    start_odometer = db.Column(db.Float)
    end_odometer = db.Column(db.Float)

    status = db.Column(
        db.Enum(TripStatus),
        default=TripStatus.DRAFT,
        nullable=False
    )

    # Relationships
    vehicle = db.relationship("Vehicle", backref="trips")
    driver = db.relationship("Driver", backref="trips")

    def distance_travelled(self):
        if self.end_odometer and self.start_odometer:
            return self.end_odometer - self.start_odometer
        return 0