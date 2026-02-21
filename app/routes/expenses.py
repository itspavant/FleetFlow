from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy import func, or_
from app.extensions import db
from app.models.trip import Trip
from app.models.fuel import FuelLog
from app.models.maintenance import MaintenanceLog
from app.models.enums import TripStatus
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.enums import UserRole
from app.utils.permissions import role_required

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")


@expenses_bp.route("/")
@login_required
def expense_dashboard():

    search = request.args.get("search")
    sort = request.args.get("sort")

    query = Trip.query.join(Trip.vehicle).join(Trip.driver).filter(
        Trip.status == TripStatus.COMPLETED
    )

    # 🔍 SEARCH (trip id / driver / vehicle)
    if search:
        query = query.filter(
            or_(
                Vehicle.model.ilike(f"%{search}%"),
                Driver.name.ilike(f"%{search}%"),
                Trip.id.like(f"%{search}%")
            )
        )

    # 🔃 SORT
    if sort == "asc":
        query = query.order_by(Trip.id.asc())
    else:
        query = query.order_by(Trip.id.desc())

    trips = query.all()

    summary = []

    for t in trips:

        fuel_cost = db.session.query(
            func.sum(FuelLog.cost)
        ).filter(
            FuelLog.trip_id == t.id
        ).scalar() or 0

        maintenance_cost = db.session.query(
            func.sum(MaintenanceLog.cost)
        ).filter(
            MaintenanceLog.vehicle_id == t.vehicle_id
        ).scalar() or 0

        distance = 0
        if t.end_odometer and t.start_odometer:
            distance = t.end_odometer - t.start_odometer

        summary.append({
            "trip": t,
            "fuel": fuel_cost,
            "maintenance": maintenance_cost,
            "distance": distance
        })

    return render_template(
        "expenses/dashboard.html",
        summary=summary
    )