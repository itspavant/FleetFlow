from app.extensions import db
from app.models.base import BaseModel
from app.models.enums import MaintenanceStatus

class MaintenanceLog(BaseModel):
    __tablename__ = "maintenance_logs"

    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)

    description = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    remarks = db.Column(db.String(255))

    status = db.Column(
        db.Enum(MaintenanceStatus),
        default=MaintenanceStatus.OPEN,
        nullable=False
    )

    vehicle = db.relationship("Vehicle", backref="maintenance_logs")