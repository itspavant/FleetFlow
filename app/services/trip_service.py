from app.extensions import db
from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.enums import (
    TripStatus,
    VehicleStatus,
    DriverStatus
)
from app.services.exceptions import (
    VehicleUnavailableError,
    DriverUnavailableError,
    CapacityExceededError,
    LicenseExpiredError,
    InvalidStateTransitionError
)


class TripService:

    @staticmethod
    def dispatch_trip(trip_id):
        trip = Trip.query.get(trip_id)

        if not trip:
            raise ValueError("Trip not found")

        if trip.status != TripStatus.DRAFT:
            raise InvalidStateTransitionError(
                "Only draft trips can be dispatched"
            )

        vehicle = trip.vehicle
        driver = trip.driver

        # 1️⃣ Vehicle must be available
        if vehicle.status != VehicleStatus.AVAILABLE:
            raise VehicleUnavailableError(
                "Vehicle is not available"
            )

        # 2️⃣ Driver must be on duty
        if driver.status != DriverStatus.ON_DUTY:
            raise DriverUnavailableError(
                "Driver is not on duty"
            )

        # 3️⃣ Cargo capacity check
        if trip.cargo_weight > vehicle.max_capacity:
            raise CapacityExceededError(
                "Cargo exceeds vehicle capacity"
            )

        # 4️⃣ License validity
        if not driver.is_license_valid():
            raise LicenseExpiredError(
                "Driver license is expired"
            )

        # 5️⃣ State updates
        trip.status = TripStatus.DISPATCHED
        vehicle.status = VehicleStatus.ON_TRIP
        driver.status = DriverStatus.ON_TRIP

        trip.start_odometer = vehicle.odometer

        db.session.commit()

        return trip

    @staticmethod
    def complete_trip(trip_id, end_odometer):
        trip = Trip.query.get(trip_id)

        if not trip:
            raise ValueError("Trip not found")

        if trip.status != TripStatus.DISPATCHED:
            raise InvalidStateTransitionError(
                "Only dispatched trips can be completed"
            )

        if end_odometer <= trip.start_odometer:
            raise ValueError("Invalid odometer reading")

        vehicle = trip.vehicle
        driver = trip.driver

        # Update trip
        trip.end_odometer = end_odometer
        trip.status = TripStatus.COMPLETED

        # Update vehicle
        vehicle.odometer = end_odometer
        vehicle.status = VehicleStatus.AVAILABLE

        # Update driver
        driver.status = DriverStatus.ON_DUTY

        db.session.commit()

        return trip