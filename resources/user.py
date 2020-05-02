from flask_restplus import Resource, Namespace, fields
from flask import jsonify
from security import token_required
from models.user import User 

register_ns = Namespace('register')
user_model = register_ns.model("User",{"username":fields.String("first name"),"password":fields.String("a secret password")})

#@register_ns.route("/register")
class Register(Resource):

    #@register_ns.doc(security='apikey')
    #@token_required
    def get(self):
        return User.get_users()

    @register_ns.expect(user_model,envelope="The user")
    def post(self):
        data = register_ns.payload
        user = User(**data)
        user.save_to_db()
        return jsonify({"message":"User added"})

    @register_ns.expect(user_model)
    #@register_ns.doc(security='apikey')
    #@token_required
    def put(self):

        data = register_ns.payload
        user = User.find_user_by_username(data["username"])

        if user:
            user.password = data["password"]
            user.save_to_db()
            return jsonify({"message":"User updated"})

        return jsonify({"message":"User not found"}),404

    @register_ns.expect(user_model)
    #@register_ns.doc(security='apikey')
    #@token_required
    def delete(self):
        data = register_ns.payload
        user = User.find_user_by_username(data["username"])

        if user:
            user.delete_from_db()
            return jsonify({"message":"User deleted"})
        return jsonify({"message":"User not found"}),404