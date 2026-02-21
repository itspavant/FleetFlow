from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.models.fuel import FuelLog
from app.models.trip import Trip
from datetime import datetime

fuel_bp = Blueprint("fuel", __name__, url_prefix="/fuel")


@fuel_bp.route("/add/<int:trip_id>", methods=["GET", "POST"])
@login_required
def add_fuel(trip_id):
    trip = Trip.query.get_or_404(trip_id)

    if request.method == "POST":
        liters = float(request.form["liters"])
        cost = float(request.form["cost"])
        date = datetime.strptime(
            request.form["date"], "%Y-%m-%d"
        ).date()

        fuel = FuelLog(
            trip_id=trip_id,
            liters=liters,
            cost=cost,
            date=date
        )

        db.session.add(fuel)
        db.session.commit()

        flash("Fuel log added.")
        return redirect(url_for("trips.list_trips"))

    return render_template("fuel/add.html", trip=trip)