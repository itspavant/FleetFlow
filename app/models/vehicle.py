from app.extensions import db
from app.models.base import BaseModel
from app.models.enums import VehicleStatus


class Vehicle(BaseModel):
    __tablename__ = "vehicles"

    name = db.Column(db.String(100), nullable=False)
    license_plate = db.Column(db.String(50), unique=True, nullable=False)
    max_capacity = db.Column(db.Float, nullable=False)
    odometer = db.Column(db.Float, default=0)
    acquisition_cost = db.Column(db.Float, nullable=False)

    status = db.Column(
        db.Enum(VehicleStatus),
        default=VehicleStatus.AVAILABLE,
        nullable=False
    )