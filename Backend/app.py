import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

# Flask ilovasini yaratish
app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

# .env faylidan o'zgarmas ma'lumotlarni yuklash
load_dotenv()

# Swagger URL va JSON fayli
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

# Swagger UI blueprintni ro'yxatdan o'tkazish
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swaggerni sozlash
        'app_name': "Personal Finance Manager API"
    }
)

# Swagger UI blueprintni Flask ilovasiga qo'shish
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# JWT va SQLAlchemy konfiguratsiyasi
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecretkey")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flaskuser:0955@localhost/personal_finance_manager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Foydalanuvchilar jadvali
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

# Ro'yxatdan o'tish API
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    print(data)

    if not username or not email or not password:
        return jsonify({'msg': "Hamma maydonlar to'ldirilishi kerak!"}), 400

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({'msg': "Bu username yoki email allaqachon mavjud!"}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'msg': "Ro'yxatdan o'tish muvaffaqiyatli amalga oshirildi!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': f"Xato yuz berdi: {str(e)}"}), 500

# Login API
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'msg': "Username va password talab qilinadi"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'msg': "Noto‘g‘ri username yoki parol"}), 401

    token = create_access_token(identity=username)
    return jsonify(access_token=token), 200

# Himoyalangan API
@app.route('/api/auth/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Xush kelibsiz, {current_user}!"})

# Flask ilovasini ishga tushirish
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Bazadagi jadvallarni yaratish
    app.run(debug=True)
