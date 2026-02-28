# IMPERIAL HOUSE - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Command Line Installation

```bash
# 1. Navigate to project
cd c:\tennis_payment_system

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
copy .env.example .env

# 5. Initialize database
python run.py
# Then open browser: http://localhost:5000

# CTRL+C to stop server
```

### Option 2: Using PowerShell

```powershell
cd c:\tennis_payment_system
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python run.py
```

## 📝 First Time Setup

1. **Create Sample Users** (Optional)
   ```bash
   flask shell
   from app.models import db, User
   
   # Create landlord
   landlord = User(username='landlord1', email='landlord1@test.com', phone='0718357417', full_name='John', user_type='landlord')
   landlord.set_password('password123')
   db.session.add(landlord)
   
   # Create tenant
   tenant = User(username='tenant1', email='tenant1@test.com', phone='0700000001', full_name='Jane', user_type='tenant')
   tenant.set_password('password123')
   db.session.add(tenant)
   
   db.session.commit()
   exit()
   ```

2. **Test the Application**
   - Open http://localhost:5000
   - Register as a Landlord or Tenant
   - Or login with sample credentials above

## 🏠 Landlord Workflow

1. Register as Landlord
2. Click "Add New House"
3. **Step 1**: Enter property details (title, description, rent, location)
   - Get latitude/longitude from Google Maps
   - Example: Nairobi Coffee House = -1.2921, 36.8219
4. **Step 2**: Upload property photos
   - Minimum 1 photo required
   - First photo becomes main image
5. **Step 3**: Complete payment
   - Choose payment method (M-PESA, Airtel, or CO-OP Bank)
   - Amount: KES 5,000
   - Enter transaction reference code
   - Property auto-publishes after verification

## 🔍 Tenant Workflow

1. Register as Tenant
2. Browse properties on home page or click "Search"
3. Use filters to find properties:
   - By city
   - By price range
   - By bedrooms/bathrooms
4. Click property to view:
   - Full details
   - All photos
   - Exact location on map
   - Landlord contact info
5. Features:
   - Add to favorites (click heart icon)
   - Send message to landlord
   - View landlord profile

## 🔐 Test Credentials

**Landlord**
- Username: landlord1
- Password: password123

**Tenant**
- Username: tenant1
- Password: password123

## 💰 Payment Methods

### M-PESA
- Number: 0718357417
- Steps in app show exact instructions

### Airtel Money
- Number: 0103633071
- Steps in app show exact instructions

### CO-OP Bank
- Paybill: 400200
- Account: 01102672539001
- Steps in app show exact instructions

*Note: In development mode, payments are simulated. In production, integrate with actual payment APIs.*

## 📂 Project Structure

```
app/
├── models.py         # Database models
├── routes.py         # All routes (auth, main, landlord, tenant, payment)
├── payments.py       # Payment processing
├── utils.py          # Helper functions
├── config.py         # Configuration
├── templates/        # HTML templates
└── static/           # CSS, JS, uploads

run.py               # Start here
requirements.txt     # Dependencies
```

## 🔗 Important URLs

| Page | URL |
|------|-----|
| Home | http://localhost:5000/ |
| Login | http://localhost:5000/auth/login |
| Register | http://localhost:5000/auth/register |
| Landlord Dashboard | http://localhost:5000/landlord/dashboard |
| Tenant Dashboard | http://localhost:5000/tenant/dashboard |
| Search Houses | http://localhost:5000/tenant/search |
| Add House | http://localhost:5000/landlord/add-house-step-1 |

## ⚙️ Configuration

Edit `.env` file to change:
- Database URL
- Secret key
- Payment amounts
- Payment phone numbers

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use different port:
python run.py -p 5001
# Or in run.py change port=5000 to port=5001
```

### Database Issues
```bash
# Reset database:
# Delete imperialhouse.db file
# Run: python run.py
# It will create a new database
```

### Virtual Environment Issues
```bash
# Deactivate and remove venv:
deactivate
rmdir /s venv
# Then recreate it
```

## 📞 Support

Payment Methods Contact:
- **M-PESA**: 0718357417
- **Airtel Money**: 0103633071
- **CO-OP Bank**: 400200 / 01102672539001

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created
- [ ] Application running (`python run.py`)
- [ ] Accessed http://localhost:5000
- [ ] Created test users
- [ ] Tested landlord flow
- [ ] Tested tenant flow

---

**You're all set! Happy house hunting! 🏠❤️**
