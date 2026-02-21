from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func
from datetime import datetime
from app.extensions import db
from app.models.trip import Trip
from app.models.fuel import FuelLog
from app.models.trip_expense import TripExpense
from app.models.enums import TripStatus

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.route("/")
@login_required
def view_analytics():

    completed_trips = Trip.query.filter(
        Trip.status == TripStatus.COMPLETED
    ).all()

    total_revenue = sum(t.revenue or 0 for t in completed_trips)

    total_fuel = db.session.query(
        func.sum(FuelLog.cost)
    ).scalar() or 0

    total_misc = db.session.query(
        func.sum(TripExpense.amount)
    ).scalar() or 0

    total_cost = total_fuel + total_misc

    roi = 0
    if total_cost:
        roi = round(((total_revenue - total_cost) / total_cost) * 100, 2)

    # ----------------------
    # Chart 1: Revenue vs Cost
    # ----------------------

    chart_labels = ["Revenue", "Cost"]
    chart_values = [total_revenue, total_cost]

    # ----------------------
    # Chart 2: Top 5 Costliest Trips
    # ----------------------

    trip_costs = []

    for t in completed_trips:
        fuel = db.session.query(func.sum(FuelLog.cost)).filter(
            FuelLog.trip_id == t.id
        ).scalar() or 0

        misc = db.session.query(func.sum(TripExpense.amount)).filter(
            TripExpense.trip_id == t.id
        ).scalar() or 0

        trip_costs.append((t.id, fuel + misc))

    trip_costs.sort(key=lambda x: x[1], reverse=True)

    top_5 = trip_costs[:5]

    top_labels = [f"Trip {t[0]}" for t in top_5]
    top_values = [t[1] for t in top_5]

    # ----------------------
    # Monthly Summary
    # ----------------------

    current_month = datetime.now().month

    monthly_revenue = 0
    monthly_fuel = 0
    monthly_misc = 0

    for t in completed_trips:
        if t.created_at and t.created_at.month == current_month:
            monthly_revenue += t.revenue or 0

    monthly_fuel = db.session.query(
        func.sum(FuelLog.cost)
    ).filter(
        func.month(FuelLog.date) == current_month
    ).scalar() or 0

    monthly_misc = db.session.query(
        func.sum(TripExpense.amount)
    ).filter(
        func.month(TripExpense.date) == current_month
    ).scalar() or 0

    monthly_profit = monthly_revenue - (monthly_fuel + monthly_misc)

    return render_template(
        "analytics/dashboard.html",
        total_fuel=total_fuel,
        roi=roi,
        total_revenue=total_revenue,
        chart_labels=chart_labels,
        chart_values=chart_values,
        top_labels=top_labels,
        top_values=top_values,
        monthly_revenue=monthly_revenue,
        monthly_fuel=monthly_fuel,
        monthly_misc=monthly_misc,
        monthly_profit=monthly_profit
    )