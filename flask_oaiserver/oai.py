from flask import Flask
import config

app = Flask(__name__)
app.debug = True
app.config.from_object(config)
try:
    app.config['CFG_SITE_URL']
except:
    app.config['CFG_SITE_URL'] = "http://localhost"

from .views.server import blueprint as server
from .views.settings import blueprint as settings

app.register_blueprint(server)
app.register_blueprint(settings)

if __name__ == '__main__':
    app.run()
