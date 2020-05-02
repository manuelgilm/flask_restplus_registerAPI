from functools import wraps
from flask import request 

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):

        token = None
        
        if 'X-API-KEY' in request.headers:
            token = request.headers["X-API-KEY"]

        if not token:
            return {"message":"Token is missing"}, 401
        
        if token != "666":
            return {"message":"Your token is wrong"},401

        return f(*args,**kwargs)
    return decorated

