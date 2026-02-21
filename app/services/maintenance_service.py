from app.extensions import db
from app.models.maintenance import MaintenanceLog
from app.models.vehicle import Vehicle
from app.models.enums import (
    MaintenanceStatus,
    VehicleStatus
)
from app.services.exceptions import InvalidStateTransitionError


class MaintenanceService:

    @staticmethod
    def create_maintenance(vehicle_id, description, cost):
        vehicle = Vehicle.query.get(vehicle_id)

        if not vehicle:
            raise ValueError("Vehicle not found")

        if vehicle.status == VehicleStatus.ON_TRIP:
            raise InvalidStateTransitionError(
                "Cannot send vehicle to maintenance while on trip"
            )

        # Create log
        maintenance = MaintenanceLog(
            vehicle_id=vehicle_id,
            description=description,
            cost=cost,
            status=MaintenanceStatus.OPEN
        )

        # Update vehicle status
        vehicle.status = VehicleStatus.IN_SHOP

        db.session.add(maintenance)
        db.session.commit()

        return maintenance

    @staticmethod
    def complete_maintenance(maintenance_id):
        maintenance = MaintenanceLog.query.get(maintenance_id)

        if not maintenance:
            raise ValueError("Maintenance record not found")

        if maintenance.status != MaintenanceStatus.OPEN:
            raise InvalidStateTransitionError(
                "Maintenance already completed"
            )

        vehicle = maintenance.vehicle

        # Update maintenance
        maintenance.status = MaintenanceStatus.COMPLETED

        # Restore vehicle availability
        vehicle.status = VehicleStatus.AVAILABLE

        db.session.commit()

        return maintenance