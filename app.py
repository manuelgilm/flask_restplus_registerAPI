import os

from flask import Flask, jsonify
from flask_restplus import Api

from models.user import User
from resources.user import register_ns, Register

from security import token_required
from db import db

app = Flask(__name__)

authorizations = {
    'apikey':{
        'type':'apiKey',
        'in':'header',
        'name':'X-API-KEY'
    }
}

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app,authorizations=authorizations)
api.add_namespace(register_ns)
api.add_resource(Register,"/register")

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    db.init_app(app)
    app.run()