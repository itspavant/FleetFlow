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


from app.models.trip_expense import TripExpense

@expenses_bp.route("/")
@login_required
def expense_dashboard():

    search = request.args.get("search")
    sort = request.args.get("sort")

    query = Trip.query.filter(
        Trip.status == TripStatus.COMPLETED
    ).join(Trip.driver).join(Trip.vehicle)

    if search:
        query = query.filter(
            (Driver.name.ilike(f"%{search}%")) |
            (Vehicle.model.ilike(f"%{search}%")) |
            (Trip.id.like(f"%{search}%"))
        )

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

        misc_cost = db.session.query(
            func.sum(TripExpense.amount)
        ).filter(
            TripExpense.trip_id == t.id
        ).scalar() or 0

        distance = 0
        if t.end_odometer and t.start_odometer:
            distance = t.end_odometer - t.start_odometer

        summary.append({
            "trip": t,
            "fuel": fuel_cost,
            "misc": misc_cost,
            "distance": distance
        })

    return render_template(
        "expenses/dashboard.html",
        summary=summary
    )


@expenses_bp.route("/add/<int:trip_id>", methods=["GET", "POST"])
@login_required
@role_required(UserRole.MANAGER, UserRole.DISPATCHER)
def add_misc_expense(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    # 🚫 Block if not completed BEFORE anything
    if trip.status != TripStatus.COMPLETED:
        flash("Misc expense can only be added to completed trips.", "warning")
        return redirect(url_for("expenses.expense_dashboard"))

    if request.method == "POST":

        description = request.form["description"]
        amount = float(request.form["amount"])

        expense = TripExpense(
            trip_id=trip.id,
            description=description,
            amount=amount
        )

        db.session.add(expense)
        db.session.commit()

        flash("Misc expense added successfully.", "success")

        return redirect(url_for("expenses.expense_dashboard"))

    return render_template("expenses/add.html", trip=trip)