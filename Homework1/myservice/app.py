import os
from flakon import create_app
from myservice.views import blueprints
from flask_profiler import Profiler

_HERE = os.path.dirname(__file__)
_SETTINGS = os.path.join(_HERE, 'settings.ini')

app = create_app(blueprints=blueprints, settings=_SETTINGS)
app.config["DEBUG"] = True

app.config["flask_profiler"] = {
    "enabled": app.config["DEBUG"],
    "storage": {
        "engine": "sqlite"
    },
    "basicAuth": {
        "enabled": True,
        "username": "admin",
        "password": "admin"
    },
    "ignore": [
        "^/static/.*"
    ]
}

profiler = Profiler(app)  # You can have this in another module


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
