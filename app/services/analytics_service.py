from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.models.fuel import FuelLog
from app.models.maintenance import MaintenanceLog
from app.models.enums import TripStatus, MaintenanceStatus
from app.extensions import db
from sqlalchemy import func


class AnalyticsService:

    @staticmethod
    def total_revenue(vehicle_id):
        revenue = (
            db.session.query(func.sum(Trip.revenue))
            .filter(
                Trip.vehicle_id == vehicle_id,
                Trip.status == TripStatus.COMPLETED
            )
            .scalar()
        )
        return revenue or 0

    @staticmethod
    def total_fuel_cost(vehicle_id):
        fuel_cost = (
            db.session.query(func.sum(FuelLog.cost))
            .join(Trip, FuelLog.trip_id == Trip.id)
            .filter(
                Trip.vehicle_id == vehicle_id,
                Trip.status == TripStatus.COMPLETED
            )
            .scalar()
        )
        return fuel_cost or 0

    @staticmethod
    def total_maintenance_cost(vehicle_id):
        maintenance_cost = (
            db.session.query(func.sum(MaintenanceLog.cost))
            .filter(
                MaintenanceLog.vehicle_id == vehicle_id,
                MaintenanceLog.status == MaintenanceStatus.COMPLETED
            )
            .scalar()
        )
        return maintenance_cost or 0

    @staticmethod
    def vehicle_roi(vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)

        if not vehicle:
            raise ValueError("Vehicle not found")

        revenue = AnalyticsService.total_revenue(vehicle_id)
        fuel = AnalyticsService.total_fuel_cost(vehicle_id)
        maintenance = AnalyticsService.total_maintenance_cost(vehicle_id)

        total_cost = fuel + maintenance

        if vehicle.acquisition_cost == 0:
            return 0

        roi = (revenue - total_cost) / vehicle.acquisition_cost
        return roi

    @staticmethod
    def fuel_efficiency(vehicle_id):
        trips = Trip.query.filter(
            Trip.vehicle_id == vehicle_id,
            Trip.status == TripStatus.COMPLETED
        ).all()

        total_distance = 0
        total_liters = 0

        for trip in trips:
            total_distance += trip.distance_travelled()
            for fuel in trip.fuel_logs:
                total_liters += fuel.liters

        if total_liters == 0:
            return 0

        return total_distance / total_liters