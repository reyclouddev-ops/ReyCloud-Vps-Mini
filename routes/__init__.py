from .auth import auth
from .dashboard import dashboard
from .server import server

def register_routes(app):

    app.register_blueprint(auth)

    app.register_blueprint(dashboard)

    app.register_blueprint(server)
