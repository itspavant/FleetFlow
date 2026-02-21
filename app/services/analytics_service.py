from app.models.trip import Trip
from app.models.fuel import FuelLog
from app.models.maintenance import MaintenanceLog
from app.models.vehicle import Vehicle
from app.models.enums import TripStatus


class AnalyticsService:

    @staticmethod
    def total_revenue(vehicle_id=None):
        query = Trip.query.filter(
            Trip.status == TripStatus.COMPLETED
        )

        if vehicle_id:
            query = query.filter(Trip.vehicle_id == vehicle_id)

        return sum(trip.revenue for trip in query.all())

    @staticmethod
    def total_fuel_cost(vehicle_id=None):
        if vehicle_id:
            trips = Trip.query.filter_by(vehicle_id=vehicle_id).all()
            trip_ids = [t.id for t in trips]
            logs = FuelLog.query.filter(
                FuelLog.trip_id.in_(trip_ids)
            ).all()
        else:
            logs = FuelLog.query.all()

        return sum(log.cost for log in logs)

    @staticmethod
    def total_maintenance_cost(vehicle_id=None):
        if vehicle_id:
            logs = MaintenanceLog.query.filter_by(
                vehicle_id=vehicle_id
            ).all()
        else:
            logs = MaintenanceLog.query.all()

        return sum(log.cost for log in logs)

    @staticmethod
    def vehicle_profit(vehicle_id):
        revenue = AnalyticsService.total_revenue(vehicle_id)
        fuel = AnalyticsService.total_fuel_cost(vehicle_id)
        maintenance = AnalyticsService.total_maintenance_cost(vehicle_id)

        return revenue - fuel - maintenance

    @staticmethod
    def vehicle_roi(vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle or vehicle.acquisition_cost == 0:
            return 0

        profit = AnalyticsService.vehicle_profit(vehicle_id)
        return round((profit / vehicle.acquisition_cost) * 100, 2)

    @staticmethod
    def fuel_efficiency(vehicle_id):
        trips = Trip.query.filter_by(
            vehicle_id=vehicle_id,
            status=TripStatus.COMPLETED
        ).all()

        total_distance = sum(
            (t.end_odometer - t.start_odometer)
            for t in trips
            if t.end_odometer and t.start_odometer
        )

        fuel_logs = []
        for t in trips:
            fuel_logs.extend(t.fuel_logs)

        total_liters = sum(log.liters for log in fuel_logs)

        if total_liters == 0:
            return 0

        return round(total_distance / total_liters, 2)