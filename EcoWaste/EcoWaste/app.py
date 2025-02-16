from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import os
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import urllib.parse
import random
from GreenTalk import classify_intent, responses

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
# Database configuration
password = urllib.parse.quote_plus('Mano@123')  # Properly encode the password
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{password}@localhost/ecowaste'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize ML models as None
model = None
product_encoder = None
brand_encoder = None
usage_encoder = None

# Try to load ML models
try:
    print("Loading ML models...")
    model = joblib.load('fixed_multi_output_model.pkl')
    product_encoder = joblib.load('product_encoder.pkl')
    brand_encoder = joblib.load('brand_encoder.pkl')
    usage_encoder = joblib.load('usage_encoder.pkl')
    print("ML models loaded successfully!")
except Exception as e:
    print(f"Warning: ML models not loaded. Prediction features will be disabled. Error: {str(e)}")

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'individual', 'retailer', or 'business'
    
    # Common fields
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    
    # Individual-specific fields
    eco_points = db.Column(db.Integer, default=0)
    
    # Retailer-specific fields
    store_name = db.Column(db.String(100))
    business_license = db.Column(db.String(50))
    
    # Business-specific fields
    company_name = db.Column(db.String(100))
    industry_type = db.Column(db.String(50))
    employee_count = db.Column(db.String(20))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_type = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    usage_pattern = db.Column(db.String(50), nullable=False)
    predicted_expiry = db.Column(db.Float, nullable=False)
    predicted_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Page Routes
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/submit')
def submit_page():
    return render_template('submit.html')

@app.route('/login')
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register')
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/rewards')
def rewards_page():
    return render_template('rewards.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

# API Routes
@app.route('/api/predict', methods=['POST'])
@login_required
def predict():
    try:
        # Check if ML models are loaded
        if not all([model, product_encoder, brand_encoder, usage_encoder]):
            return jsonify({
                'error': 'ML models not loaded. Prediction feature is currently disabled.'
            }), 503
            
        data = request.json
        
        # Transform input data
        input_data = pd.DataFrame({
            'Product_Type': [product_encoder.transform([data['product_type']])[0]],
            'Brand': [brand_encoder.transform([data['brand']])[0]],
            'Usage_Pattern': [usage_encoder.transform([data['usage_pattern']])[0]]
        })
        
        # Make prediction
        prediction = model.predict(input_data)
        
        # Create new product record
        new_product = Product(
            product_type=data['product_type'],
            brand=data['brand'],
            usage_pattern=data['usage_pattern'],
            predicted_expiry=float(prediction[0][0]),
            predicted_price=float(prediction[0][1]),
            user_id=current_user.id
        )
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({
            'expiry_years': float(prediction[0][0]),
            'current_price': float(prediction[0][1])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
            
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400

        # Hash the password
        hashed_password = generate_password_hash(data['password'], method='sha256')

        # Common user data
        new_user = User(
            username=data['username'],
            password=hashed_password,
            email=data['email'],
            user_type=data['user_type'],
            full_name=data.get('full_name'),
            phone=data.get('phone'),
            address=data.get('address')
        )

        # Add type-specific fields
        if data['user_type'] == 'individual':
            new_user.eco_points = 0
        elif data['user_type'] == 'retailer':
            new_user.store_name = data.get('store_name')
            new_user.business_license = data.get('business_license')
        elif data['user_type'] == 'business':
            new_user.company_name = data.get('company_name')
            new_user.industry_type = data.get('industry_type')
            new_user.employee_count = data.get('employee_count')

        db.session.add(new_user)
        db.session.commit()

        # Log the user in after registration
        login_user(new_user)
        
        return jsonify({
            'message': 'User created successfully',
            'user_type': new_user.user_type
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        if check_password_hash(user.password, data['password']):
            login_user(user)
            return jsonify({
                'message': 'Logged in successfully',
                'user_type': user.user_type
            })
        
        return jsonify({'error': 'Invalid password'}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == 'individual':
        return render_template('dashboards/individual-dashboard.html', user=current_user)
    elif current_user.user_type == 'retailer':
        return render_template('dashboards/retailer-dashboard.html', user=current_user)
    elif current_user.user_type == 'business':
        return render_template('dashboards/company-dashboard.html', user=current_user)
    return redirect(url_for('home'))

@app.route('/api/products', methods=['GET'])
@login_required
def get_products():
    products = Product.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': p.id,
        'product_type': p.product_type,
        'brand': p.brand,
        'usage_pattern': p.usage_pattern,
        'predicted_expiry': p.predicted_expiry,
        'predicted_price': p.predicted_price,
        'created_at': p.created_at.isoformat()
    } for p in products])

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        # Get intent from GreenTalk
        intent = classify_intent(user_message)
        
        # Get response based on intent
        response_list = responses.get(intent, responses['unknown'])
        response = random.choice(response_list)
        
        return jsonify({
            'response': response
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
    
    print("\nStarting EcoWaste Server...")
    print("Available routes:")
    print("  - / (GET): Home")
    print("  - /submit (GET): Submit page")
    print("  - /login (GET): Login page")
    print("  - /register (GET): Register page")
    print("  - /rewards (GET): Rewards page")
    print("  - /about (GET): About page")
    print("  - /chatbot (GET): Chatbot page")
    print("  - /api/predict (POST): Make predictions")
    print("  - /api/register (POST): Register new user")
    print("  - /api/login (POST): Login user")
    print("  - /api/logout (GET): Logout user")
    print("  - /api/products (GET): Get user's product history")
    print("  - /api/chat (POST): Chat with the chatbot")
    print("\nServer is running on http://localhost:5000")
    
    app.run(debug=True, port=5000)
