from flask import Flask
from routes import routes_bp
from database import db
import os

def create_app():
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///careergo.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(routes_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
