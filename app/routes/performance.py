from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func
from datetime import date
from app.models.trip import Trip
from app.models.enums import TripStatus
from app.models.driver import Driver

performance_bp = Blueprint("performance", __name__, url_prefix="/performance")


from flask import request
from datetime import date

@performance_bp.route("/")
@login_required
def performance_dashboard():

    search = request.args.get("search", "")
    compliance = request.args.get("compliance", "all")

    drivers = Driver.query.all()
    performance_data = []

    for driver in drivers:

        total_trips = Trip.query.filter(
            Trip.driver_id == driver.id,
            Trip.status != TripStatus.CANCELLED
        ).count()

        completed_trips = Trip.query.filter(
            Trip.driver_id == driver.id,
            Trip.status == TripStatus.COMPLETED
        ).count()

        completion_rate = 0

        if total_trips > 0:
            completion_rate = round((completed_trips / total_trips) * 100, 2)

        expired = driver.license_expiry_date < date.today()

        performance_data.append({
            "driver": driver,
            "total_trips": total_trips,
            "completed_trips": completed_trips,
            "completion_rate": completion_rate,
            "expired": expired
        })

    # 🔎 SEARCH FILTER
    if search:
        performance_data = [
            d for d in performance_data
            if search.lower() in d["driver"].name.lower()
        ]

    # 📋 COMPLIANCE FILTER
    if compliance == "compliant":
        performance_data = [d for d in performance_data if not d["expired"]]
    elif compliance == "noncompliant":
        performance_data = [d for d in performance_data if d["expired"]]

    return render_template(
        "performance/dashboard.html",
        performance_data=performance_data,
        search=search,
        compliance=compliance
    )