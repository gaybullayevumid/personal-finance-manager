import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS  # CORS ni import qilamiz

# Flask ilovasini yaratamiz
app = Flask(__name__)
CORS(app)  # Frontend bilan ishlash uchun CORS ni yoqamiz

# Muhit o‘zgaruvchilarini yuklash
load_dotenv()

# JWT konfiguratsiyasi
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecretkey")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # Token 1 soat amal qiladi
jwt = JWTManager(app)

# Foydalanuvchi bazasi (oddiy lug‘at sifatida)
users = {
    "john": generate_password_hash("1234")  # Login: "john", Parol: "1234"
}


# 🔹 LOGIN API (Foydalanuvchini tizimga kirishi)
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"msg": "Username va password talab qilinadi"}), 400

    username = data["username"]
    password = data["password"]

    if username not in users:
        return jsonify({"msg": "Foydalanuvchi topilmadi"}), 404

    if not check_password_hash(users[username], password):
        return jsonify({"msg": "Noto‘g‘ri parol"}), 401

    token = create_access_token(identity=username)
    return jsonify(access_token=token), 200


# 🔹 HIMOYALANGAN SAHIFA (Token talab qilinadi)
@app.route('/api/auth/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Xush kelibsiz, {current_user}!"})


# Flask serverni ishga tushiramiz
if __name__ == '__main__':
    app.run(debug=True)
