from flask import Flask
from config import Config
from database import db
from routes import routes_bp
from careergo.auth import auth, login_manager

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(routes_bp)
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True)
