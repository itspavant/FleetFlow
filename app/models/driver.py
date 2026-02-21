from app.extensions import db
from app.models.base import BaseModel
from app.models.enums import DriverStatus
from datetime import date


class Driver(BaseModel):
    __tablename__ = "drivers"

    name = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(100), unique=True, nullable=False)
    license_category = db.Column(db.String(50), nullable=False)
    license_expiry_date = db.Column(db.Date, nullable=False)

    safety_score = db.Column(db.Float, default=100.0)

    status = db.Column(
        db.Enum(DriverStatus),
        default=DriverStatus.ON_DUTY,
        nullable=False
    )

    def is_license_valid(self):
        return self.license_expiry_date >= date.today()