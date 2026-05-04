import os
from flask import Flask
from app.routes import recipe_bp

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev')
    )

    app.register_blueprint(recipe_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
