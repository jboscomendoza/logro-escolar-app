from app import app

with app.app_context():
    # Import Dash application
    from dashboard.dashboard import create_dashboard
    app = create_dashboard(app)