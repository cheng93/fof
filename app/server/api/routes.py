from api.teams import routes as teams_routes

def setup_routes(app):
    app.router.add_routes(teams_routes)