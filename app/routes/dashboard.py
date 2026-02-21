from flask import Blueprint, render_template
from flask_login import login_required
from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.models.enums import VehicleStatus, TripStatus

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def home():
    active_fleet = Vehicle.query.filter(
        Vehicle.status == VehicleStatus.ON_TRIP
    ).count()

    maintenance_alerts = Vehicle.query.filter(
        Vehicle.status == VehicleStatus.IN_SHOP
    ).count()

    pending_trips = Trip.query.filter(
        Trip.status == TripStatus.DRAFT
    ).count()

    return render_template(
        "dashboard.html",
        active_fleet=active_fleet,
        maintenance_alerts=maintenance_alerts,
        pending_trips=pending_trips
    )