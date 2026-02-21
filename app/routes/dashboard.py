from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import or_
from datetime import date
from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.models.maintenance import MaintenanceLog
from app.models.driver import Driver
from app.models.enums import TripStatus, VehicleStatus, MaintenanceStatus

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def home():

    search_query = request.args.get("search")
    sort_option = request.args.get("sort")
    status_filter = request.args.get("status")

    # Base query
    trip_query = Trip.query

    # 🔍 SEARCH
    if search_query:
        trip_query = trip_query.join(Trip.vehicle).join(Trip.driver).filter(
            or_(
                Trip.id.like(f"%{search_query}%"),
                Vehicle.model.ilike(f"%{search_query}%"),
                Driver.name.ilike(f"%{search_query}%")
            )
        )

    # 🎯 FILTER
    if status_filter:
        trip_query = trip_query.filter(Trip.status == TripStatus[status_filter])

    # 🔃 SORT
    if sort_option == "asc":
        trip_query = trip_query.order_by(Trip.id.asc())
    elif sort_option == "desc":
        trip_query = trip_query.order_by(Trip.id.desc())
    else:
        trip_query = trip_query.order_by(Trip.id.desc())

    recent_trips = trip_query.limit(10).all()

    # KPIs
    total_vehicles = Vehicle.query.count()
    active_fleet = Vehicle.query.filter(
        Vehicle.status == VehicleStatus.ON_TRIP
    ).count()

    utilization_rate = 0
    if total_vehicles:
        utilization_rate = round((active_fleet / total_vehicles) * 100, 2)

    maintenance_alerts = MaintenanceLog.query.filter(
        MaintenanceLog.status == MaintenanceStatus.OPEN
    ).count()

    pending_trips = Trip.query.filter(
        Trip.status == TripStatus.DRAFT
    ).count()

    expired_licenses = Driver.query.filter(
        Driver.license_expiry_date < date.today()
    ).count()

    return render_template(
        "dashboard.html",
        active_fleet=active_fleet,
        maintenance_alerts=maintenance_alerts,
        pending_trips=pending_trips,
        utilization_rate=utilization_rate,
        expired_licenses=expired_licenses,
        recent_trips=recent_trips
    )