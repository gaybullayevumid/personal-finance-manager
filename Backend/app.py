from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

jwt = JWTManager(app)

users = {
    "admin": "admin",
    "password": "admin123"
}

@app.route('/api/v1/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users and users['username'] == password:
        token = create_access_token(identity=username)
        return jsonify(access_token=token)
    
    return jsonify({"msg": "Error username or password"})


@app.route('/api/v1', methods=['GET'])
def home():
    return jsonify({"message": "Hello, World!"})


if __name__ == '__main__':
    app.run(debug=True)