# IMPERIAL HOUSE - Rental Property Listing Application

A complete web application for landlords to list rental properties and tenants to find homes. Landlords pay KES 5,000 using M-PESA, Airtel Money, or CO-OP Bank to list their properties.

## Features

### For Landlords
- ✅ User registration and authentication
- ✅ Multi-step house listing (3 steps: details, photos, payment)
- ✅ Upload multiple property photos
- ✅ Automatic property posting after payment verification
- ✅ Edit and manage listings
- ✅ Receive messages from interested tenants
- ✅ Dashboard with statistics

### For Tenants
- ✅ Browse all listed properties
- ✅ Advanced search (city, price, bedrooms, bathrooms)
- ✅ View detailed property information with maps
- ✅ Save favorite properties
- ✅ Message landlords directly
- ✅ View exact property locations on map

### Payment Integration
- ✅ M-PESA: 0718357417
- ✅ Airtel Money: 0103633071
- ✅ CO-OP Bank Paybill: 400200 | Account: 01102672539001
- ✅ Payment verification system
- ✅ Automatic property publishing after payment

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **Authentication**: Flask-Login
- **Image Processing**: Pillow
- **Maps**: Leaflet.js (OpenStreetMap)

## Installation

### 1. Clone/Download the Project
```bash
cd c:\tennis_payment_system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment
```bash
copy .env.example .env
# Edit .env with your configuration
```

### 5. Initialize Database
```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

### 6. Create Sample Data (Optional)
```bash
python run.py

# Then in another terminal:
# Or manually in Flask shell:
# python -m flask create-sample-data
```

### 7. Run Application
```bash
python run.py
```

Visit http://localhost:5000 in your browser.

## Usage

### For Landlords

1. **Register**: Click "Register" and select "I am a Landlord"
2. **Add House**: 
   - Step 1: Enter property details (title, description, price, location with coordinates)
   - Step 2: Upload multiple property photos
   - Step 3: Complete payment via M-PESA, Airtel, or CO-OP Bank
3. **After Payment**: Property is automatically published and visible to tenants
4. **Manage**: Edit, delete, or view your listings from the dashboard

### For Tenants

1. **Register**: Click "Register" and select "I am a Tenant"
2. **Browse**: Use the search to find properties by city, price range, bedrooms, etc.
3. **View Details**: Click any property to see full details, photos, and exact location on map
4. **Save Favorites**: Click the heart icon to save properties
5. **Contact**: Send messages directly to landlords

## File Structure

```
imperial_house/
├── app/
│   ├── templates/          # HTML templates
│   │   ├── auth/          # Login/Register
│   │   ├── main/          # Home page, house details
│   │   ├── landlord/      # Landlord dashboards and forms
│   │   ├── tenant/        # Tenant dashboards and search
│   │   └── payment/       # Payment pages
│   ├── static/
│   │   ├── css/           # Stylesheets
│   │   ├── js/            # JavaScript files
│   │   └── uploads/       # User uploaded images
│   ├── models.py          # Database models
│   ├── routes.py          # Application routes
│   ├── payments.py        # Payment handling
│   ├── utils.py           # Utility functions
│   ├── config.py          # Configuration
│   └── __init__.py        # App initialization
├── run.py                 # Entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
└── README.md             # This file
```

## Database Schema

### Users
- Stores landlords and tenants with authentication

### Houses
- Property listings with details, price, location (lat/lon)

### HouseImages
- Multiple photos per property

### Payments
- Payment transactions with M-PESA, Airtel, CO-OP references

### Favorites
- Tenants' saved properties

### Messages
- Direct messages between landlords and tenants

## Payment Verification

**Important**: In production, implement actual payment verification with:
- M-PESA Daraja API
- Airtel Money API
- CO-OP Bank API

Currently, the app accepts transaction references and requires manual verification.

## Features Roadmap

- [ ] Admin panel for payment verification
- [ ] Email notifications
- [ ] SMS notifications
- [ ] Property reviews and ratings
- [ ] Advanced map search
- [ ] Mobile app
- [ ] Video tours
- [ ] Virtual tours
- [ ] Telegram bot integration
- [ ] WhatsApp integration

## Security Notes

- Set `SECRET_KEY` to a strong random value in production
- Use HTTPS in production
- Enable `SESSION_COOKIE_SECURE = True` in production
- Regularly update dependencies
- Implement rate limiting
- Add CSRF protection for sensitive forms

## Support

For issues or suggestions, create a GitHub issue or contact the team.

## License

This project is proprietary to IMPERIAL HOUSE.

---

**IMPERIAL HOUSE** - Find Your Perfect Home! 🏠❤️
