from app.utils.permissions import role_required
from app.models.enums import UserRole
from flask import Blueprint, render_template
from flask_login import login_required
from app.services.analytics_service import AnalyticsService
from app.models.vehicle import Vehicle


analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.route("/")
@login_required
@role_required(UserRole.MANAGER, UserRole.ANALYST)
def view_analytics():
    total_revenue = AnalyticsService.total_revenue()
    total_fuel = AnalyticsService.total_fuel_cost()
    total_maintenance = AnalyticsService.total_maintenance_cost()

    net_profit = total_revenue - total_fuel - total_maintenance

    vehicles = Vehicle.query.all()

    vehicle_data = []

    for v in vehicles:
        vehicle_data.append({
            "vehicle": v,
            "profit": AnalyticsService.vehicle_profit(v.id),
            "roi": AnalyticsService.vehicle_roi(v.id),
            "fuel_efficiency": AnalyticsService.fuel_efficiency(v.id)
        })

    return render_template(
        "analytics/dashboard.html",
        total_revenue=total_revenue,
        total_fuel=total_fuel,
        total_maintenance=total_maintenance,
        net_profit=net_profit,
        vehicle_data=vehicle_data
    )