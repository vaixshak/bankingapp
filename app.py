from flask_cors import CORS
from flask_login import login_user, logout_user, login_required, current_user
from flask import Flask, render_template, request, redirect, url_for, flash
from extensions import db, bcrypt, login_manager
from models import User, Transaction
from flask_migrate import Migrate
import random

app = Flask(__name__)
CORS(app) 
app.secret_key = 'vaishak'

# DB Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/bankdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)


with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST','OPTION'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        return {"message": "Login successful", "user_id": user.id, "account_number": user.account_number}, 200

    return {"error": "Invalid email or password"}, 401

@app.route('/register', methods=['POST','OPTION'])
def register():
    data = request.json
    email = data['email']
    password = data['password']

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"error": "Email already registered."}, 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    account_number = generate_account_number()
    new_user = User(email=email, password=hashed_password, account_number=account_number, balance=500.0)
    db.session.add(new_user)
    db.session.commit()

    return {"message": "Registration successful", "account_number": account_number}, 201

@app.route("/transaction", methods=["POST"])
@login_required
def transaction():
    from transaction_service import perform_transaction
    data = request.json
    amount = data.get("amount")
    txn_type = data.get("type")  # 'credit' or 'debit'

    return_data = perform_transaction(current_user.id, amount, txn_type)
    return return_data


@app.route('/dashboard')
@login_required

def dashboard():
    return render_template('dashboard.html')

@app.route('/user-info/<int:user_id>', methods=['GET'])
def get_user_info_by_id(user_id):
    user = User.query.get(user_id)

    if user:
        return {
            "account_number": user.account_number,
            "email": user.email,
            "balance": user.balance
        }, 200

    return {"error": "User not found"}, 404

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def generate_account_number():
    return str(random.randint(1000000000, 9999999999))


# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)

