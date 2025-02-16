# 🌿 EcoWaste - AI-Powered E-Waste Management Platform

EcoWaste is an AI-powered, end-to-end e-waste management platform that automates collection, tracking, recycling, and rewards to encourage sustainable disposal of electronic waste.

## The Problem & Solution

###  The Problem
- India generated 1.75 million metric tonnes of e-waste in 2023-24, but only 31% was properly recycled
- Consumers lack awareness & incentives to dispose of electronics responsibly
- Recyclers & repair centers face difficulties in efficiently collecting e-waste
- Expired but repairable electronics often go to waste instead of being refurbished

### The Solution
- AI-powered expiry & price prediction to guide responsible disposal
- Automated e-waste pickup system connecting users, recyclers, and refurbishers
- Instant cashback rewards for users recycling their electronics
- Secure data wiping & refurbishment options for repairable devices

## 🔄 How It Works

1. Users register their electronic products on the platform at the time of purchase
2. The system tracks expiry dates and notifies users when disposal is needed
3. Users choose to either:
   - Continue using the product
   - Request a free pickup for disposal
4. Certified recyclers & refurbishers collect the e-waste from users
5. Based on condition:
   - Reusable products → Sent for refurbishment & resale
   - Non-repairable products → Sent for proper recycling
6. Users receive cashback based on the type & condition of the e-waste
7. Leaderboard & Community Engagement to encourage sustainable practices

## 🛠️ Project Structure

### Backend (Python/Flask)
```
├── app.py                         # Main Flask application & API endpoints
├── GreenTalk.py                  # AI Chatbot implementation
├── setup_database.py             # Database initialization & setup
├── check_database.py             # Database verification tools
├── data.py                       # Data handling & processing
├── Expiary_Price_Prediction.py   # ML prediction models
├── ReciptGenerate.py            # Receipt generation system
└── requirements.txt              # Python dependencies
```

### Machine Learning Components
```
├── fixed_multi_output_model.pkl  # Main prediction model
├── brand_encoder.pkl            # Brand encoding model
├── product_encoder.pkl          # Product type encoding model
├── usage_encoder.pkl           # Usage pattern encoding model
└── expiry_price_data.csv       # Training dataset
```

### Frontend
```
├── templates/
│   ├── base.html                # Base template with common elements
│   ├── index.html              # Landing page
│   ├── login.html              # User authentication
│   ├── register.html           # User registration
│   ├── about.html             # About platform
│   ├── chatbot.html           # AI assistant interface
│   ├── rewards.html           # User rewards system
│   ├── submit.html            # Product submission
│   └── dashboards/
│       ├── company-dashboard.html    # For recycling companies
│       ├── retailer-dashboard.html   # For retail partners
│       └── individual-dashboard.html  # For individual users
│
├── static/
    ├── css/
    │   ├── chatbot.css         # Chatbot styling
    │   ├── navigation.css      # Navigation components
    │   └── corner-decorations.css # UI elements
    ├── js/
    │   └── chatbot.js         # Chatbot functionality
    └── images/                # Asset storage
```

##  Features

### 🔐 User Management
- Multi-user support (Individual, Retailer, Company)
- Secure authentication & authorization
- Role-based dashboards
- Profile management

###  Product Management
- AI-powered expiry prediction
- Smart pricing suggestions
- Product lifecycle tracking
- QR code integration

### Interactive Features
- Real-time AI chatbot support
- QR code scanning
- Image processing
- Gamified reward system

###  Business Tools
- Bulk order processing
- Inventory management
- Impact reporting
- Digital receipts

##  Technology Stack

- **Backend**: Python 3.11, Flask 2.3.3
- **Database**: MySQL 8.0
- **Frontend**: HTML5, CSS3, JavaScript
- **ML**: Scikit-learn 1.3.0, Pandas 2.0.3
- **Security**: Flask-Login, Cryptography
- **API**: RESTful Architecture

## 🚀 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ecowaste.git
   cd ecowaste
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up MySQL Database:
   ```bash
   python setup_database.py
   ```

5. Configure environment:
   Create `.env` file with:
   ```
   SECRET_KEY=your_secret_key
   DATABASE_URL=mysql://username:password@localhost/ecowaste
   ```

6. Run the application:
   ```bash
   python app.py
   ```

## 🤝 Contribution Guidelines

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Run tests
6. Submit a Pull Request

## 📞 Contact & Support

- 📧 Email: support@ecowaste.com
- 🌐 Website: [EcoWaste](https://ecowaste.com)
- 📝 Issues: [GitHub Issues](https://github.com/yourusername/ecowaste/issues)

