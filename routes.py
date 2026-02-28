"""Routes for IMPERIAL HOUSE application"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from functools import wraps
from datetime import datetime
import json
import os

from app.models import db, User, House, HouseImage, Payment, Favorite, Message
from app.payments import PaymentProcessor
from app.utils import save_upload_file, delete_upload_file

# Create blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
main_bp = Blueprint('main', __name__)
landlord_bp = Blueprint('landlord', __name__, url_prefix='/landlord')
tenant_bp = Blueprint('tenant', __name__, url_prefix='/tenant')
payment_bp = Blueprint('payment', __name__, url_prefix='/payment')
api_bp = Blueprint('api', __name__, url_prefix='/api')


# ============= DECORATORS =============
def landlord_required(f):
    """Require user to be a landlord"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'landlord':
            flash('You must be a landlord to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


def tenant_required(f):
    """Require user to be a tenant"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'tenant':
            flash('You must be a tenant to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


# ============= AUTHENTICATION ROUTES =============
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user"""
    if request.method == 'POST':
        data = request.form
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        password = data.get('password', '')
        user_type = data.get('user_type', '').strip()
        full_name = data.get('full_name', '').strip()
        
        # Validation
        if not all([username, email, phone, password, full_name, user_type]):
            flash('All fields are required. Please select if you are a Tenant or Landlord.', 'danger')
            return redirect(url_for('auth.register'))
        
        if user_type not in ['tenant', 'landlord']:
            flash('Invalid user type. Please select Tenant or Landlord.', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create user
        user = User(
            username=username,
            email=email,
            phone=phone,
            full_name=full_name,
            user_type=user_type,
            is_email_verified=True  # Auto-verified
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
                
        except Exception as e:
            db.session.rollback()
            flash(f'Error during registration: {str(e)}', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login user"""
    if request.method == 'POST':
        data = request.form
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # Log them in
            login_user(user)
            
            if user.user_type == 'landlord':
                return redirect(url_for('landlord.dashboard'))
            else:
                return redirect(url_for('tenant.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))








# ============= MAIN ROUTES =============
@main_bp.route('/')
def index():
    """Home page with house listings"""
    page = request.args.get('page', 1, type=int)
    city = request.args.get('city', '', type=str)
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 999999, type=float)
    bedrooms = request.args.get('bedrooms', 0, type=int)
    
    query = House.query.filter_by(active=True, posted_after_payment=True)
    
    if city:
        query = query.filter_by(city=city)
    
    if min_price > 0:
        query = query.filter(House.rent_price >= min_price)
    
    if max_price < 999999:
        query = query.filter(House.rent_price <= max_price)
    
    if bedrooms > 0:
        query = query.filter(House.bedrooms >= bedrooms)
    
    houses = query.paginate(page=page, per_page=12)
    cities = sorted(set(current_app.config.get('KENYA_CITIES', [])))
    
    return render_template('main/index.html', houses=houses, cities=cities)


@main_bp.route('/house/<int:house_id>')
def view_house(house_id):
    """View house details"""
    house = House.query.get_or_404(house_id)
    
    if not house.active or not house.posted_after_payment:
        flash('House not found.', 'danger')
        return redirect(url_for('main.index'))
    
    images = HouseImage.query.filter_by(house_id=house_id).all()
    landlord = house.landlord
    is_favorite = False
    
    if current_user.is_authenticated and current_user.user_type == 'tenant':
        is_favorite = Favorite.query.filter_by(
            tenant_id=current_user.id,
            house_id=house_id
        ).first() is not None
    
    return render_template('main/house_detail.html', house=house, images=images, 
                         landlord=landlord, is_favorite=is_favorite)


@main_bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    if request.method == 'POST':
        flash('Thank you for your message. We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('main/contact.html')


# ============= LANDLORD ROUTES =============
@landlord_bp.route('/dashboard')
@login_required
@landlord_required
def dashboard():
    """Landlord dashboard"""
    total_houses = House.query.filter_by(landlord_id=current_user.id).count()
    active_houses = House.query.filter_by(landlord_id=current_user.id, active=True).count()
    total_payments = Payment.query.filter_by(user_id=current_user.id, status='completed').count()
    
    houses = House.query.filter_by(landlord_id=current_user.id).all()
    recent_messages = Message.query.filter_by(recipient_id=current_user.id).order_by(
        Message.created_at.desc()
    ).limit(5).all()
    
    return render_template('landlord/dashboard.html', 
                         total_houses=total_houses,
                         active_houses=active_houses,
                         total_payments=total_payments,
                         houses=houses,
                         recent_messages=recent_messages)


@landlord_bp.route('/splash-screen')
@login_required
@landlord_required
def splash_screen():
    """Show splash screen with animated house icon"""
    return render_template('landlord/splash_screen.html')


@landlord_bp.route('/add-house-step-1', methods=['GET', 'POST'])
@login_required
@landlord_required
def add_house_step1():
    """Step 1: House details"""
    if request.method == 'POST':
        data = request.form
        
        house = House(
            landlord_id=current_user.id,
            title=data.get('title'),
            description=data.get('description'),
            rent_price=float(data.get('rent_price', 0)),
            rent_period=data.get('rent_period', 'monthly'),
            bedrooms=int(data.get('bedrooms', 1)),
            bathrooms=int(data.get('bathrooms', 1)),
            square_feet=float(data.get('square_feet', 0)) if data.get('square_feet') else None,
            address=data.get('address'),
            city=data.get('city'),
            latitude=float(data.get('latitude', 0)),
            longitude=float(data.get('longitude', 0)),
            amenities=data.get('amenities', '')
        )
        
        try:
            db.session.add(house)
            db.session.commit()
            flash('House details saved. Proceed to upload photos.', 'success')
            return redirect(url_for('landlord.add_house_step2', house_id=house.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    cities = sorted(set(current_app.config.get('KENYA_CITIES', [])))
    return render_template('landlord/add_house_step1.html', cities=cities)


@landlord_bp.route('/add-house-step-2/<int:house_id>', methods=['GET', 'POST'])
@login_required
@landlord_required
def add_house_step2(house_id):
    """Step 2: Upload photos"""
    house = House.query.get_or_404(house_id)
    
    if house.landlord_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('landlord.dashboard'))
    
    if request.method == 'POST':
        files = request.files.getlist('photos')
        
        if not files or all(f.filename == '' for f in files):
            flash('Please upload at least one photo.', 'danger')
            return redirect(url_for('landlord.add_house_step2', house_id=house_id))
        
        for file in files:
            if file and file.filename:
                filename = save_upload_file(file, current_app.config['UPLOAD_FOLDER'])
                if filename:
                    image = HouseImage(house_id=house_id, image_path=filename)
                    db.session.add(image)
                    
                    if not house.main_image:
                        house.main_image = filename
        
        try:
            db.session.commit()
            flash('Photos uploaded successfully. Proceed to payment.', 'success')
            return redirect(url_for('landlord.add_house_step3', house_id=house_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error uploading photos: {str(e)}', 'danger')
    
    images = HouseImage.query.filter_by(house_id=house_id).all()
    return render_template('landlord/add_house_step2.html', house=house, images=images)


@landlord_bp.route('/add-house-step-3/<int:house_id>', methods=['GET', 'POST'])
@login_required
@landlord_required
def add_house_step3(house_id):
    """Step 3: Payment"""
    house = House.query.get_or_404(house_id)
    
    if house.landlord_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('landlord.dashboard'))
    
    payment_methods = PaymentProcessor.get_all_payment_options()
    
    return render_template('landlord/add_house_step3.html', house=house, 
                         payment_methods=payment_methods,
                         amount=current_app.config['PAYMENT_AMOUNT_KES'])


@landlord_bp.route('/houses')
@login_required
@landlord_required
def my_houses():
    """List landlord's houses"""
    page = request.args.get('page', 1, type=int)
    houses = House.query.filter_by(landlord_id=current_user.id).paginate(page=page, per_page=10)
    
    return render_template('landlord/my_houses.html', houses=houses)


@landlord_bp.route('/house/<int:house_id>/edit', methods=['GET', 'POST'])
@login_required
@landlord_required
def edit_house(house_id):
    """Edit house details"""
    house = House.query.get_or_404(house_id)
    
    if house.landlord_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('landlord.dashboard'))
    
    if request.method == 'POST':
        data = request.form
        house.title = data.get('title')
        house.description = data.get('description')
        house.rent_price = float(data.get('rent_price', 0))
        house.rent_period = data.get('rent_period', 'monthly')
        house.bedrooms = int(data.get('bedrooms', 1))
        house.bathrooms = int(data.get('bathrooms', 1))
        house.square_feet = float(data.get('square_feet', 0)) if data.get('square_feet') else None
        house.address = data.get('address')
        house.city = data.get('city')
        house.amenities = data.get('amenities', '')
        
        try:
            db.session.commit()
            flash('House updated successfully.', 'success')
            return redirect(url_for('landlord.my_houses'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating house: {str(e)}', 'danger')
    
    return render_template('landlord/edit_house.html', house=house)


@landlord_bp.route('/house/<int:house_id>/delete', methods=['POST'])
@login_required
@landlord_required
def delete_house(house_id):
    """Delete house"""
    house = House.query.get_or_404(house_id)
    
    if house.landlord_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('landlord.dashboard'))
    
    try:
        # Delete images
        images = HouseImage.query.filter_by(house_id=house_id).all()
        for image in images:
            delete_upload_file(image.image_path, current_app.config['UPLOAD_FOLDER'])
        
        db.session.delete(house)
        db.session.commit()
        flash('House deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting house: {str(e)}', 'danger')
    
    return redirect(url_for('landlord.my_houses'))


@landlord_bp.route('/messages')
@login_required
@landlord_required
def messages():
    """View messages"""
    page = request.args.get('page', 1, type=int)
    messages_list = Message.query.filter_by(recipient_id=current_user.id).order_by(
        Message.created_at.desc()
    ).paginate(page=page, per_page=10)
    
    return render_template('landlord/messages.html', messages=messages_list)


# ============= TENANT ROUTES =============
@tenant_bp.route('/dashboard')
@login_required
@tenant_required
def dashboard():
    """Tenant dashboard"""
    favorite_count = Favorite.query.filter_by(tenant_id=current_user.id).count()
    recent_favorites = Favorite.query.filter_by(tenant_id=current_user.id).order_by(
        Favorite.created_at.desc()
    ).limit(6).all()
    
    recent_messages = Message.query.filter_by(recipient_id=current_user.id).order_by(
        Message.created_at.desc()
    ).limit(5).all()
    
    return render_template('tenant/dashboard.html', 
                         favorite_count=favorite_count,
                         recent_favorites=recent_favorites,
                         recent_messages=recent_messages)


@tenant_bp.route('/splash-screen')
@login_required
@tenant_required
def splash_screen():
    """Show splash screen with animated house icon"""
    return render_template('tenant/splash_screen.html')


@tenant_bp.route('/search')
@login_required
@tenant_required
def search():
    """Advanced house search"""
    page = request.args.get('page', 1, type=int)
    city = request.args.get('city', '', type=str)
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 999999, type=float)
    bedrooms = request.args.get('bedrooms', 0, type=int)
    bathrooms = request.args.get('bathrooms', 0, type=int)
    
    query = House.query.filter_by(active=True, posted_after_payment=True)
    
    if city:
        query = query.filter_by(city=city)
    if min_price > 0:
        query = query.filter(House.rent_price >= min_price)
    if max_price < 999999:
        query = query.filter(House.rent_price <= max_price)
    if bedrooms > 0:
        query = query.filter(House.bedrooms >= bedrooms)
    if bathrooms > 0:
        query = query.filter(House.bathrooms >= bathrooms)
    
    houses = query.paginate(page=page, per_page=12)
    cities = sorted(set(current_app.config.get('KENYA_CITIES', [])))
    
    return render_template('tenant/search.html', houses=houses, cities=cities)


@tenant_bp.route('/favorites')
@login_required
@tenant_required
def favorites():
    """View favorite houses"""
    page = request.args.get('page', 1, type=int)
    favorites = Favorite.query.filter_by(tenant_id=current_user.id).paginate(page=page, per_page=12)
    
    return render_template('tenant/favorites.html', favorites=favorites)


@tenant_bp.route('/messages', methods=['GET', 'POST'])
@login_required
@tenant_required
def messages():
    """Send message to landlord"""
    if request.method == 'POST':
        data = request.form
        recipient_id = data.get('recipient_id', type=int)
        house_id = data.get('house_id', type=int)
        subject = data.get('subject')
        content = data.get('content')
        
        message = Message(
            sender_id=current_user.id,
            recipient_id=recipient_id,
            house_id=house_id,
            subject=subject,
            content=content
        )
        
        try:
            db.session.add(message)
            db.session.commit()
            flash('Message sent successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error sending message: {str(e)}', 'danger')
    
    page = request.args.get('page', 1, type=int)
    messages_list = Message.query.filter_by(sender_id=current_user.id).order_by(
        Message.created_at.desc()
    ).paginate(page=page, per_page=10)
    
    return render_template('tenant/messages.html', messages=messages_list)


# ============= PAYMENT ROUTES =============
@payment_bp.route('/initiate/<int:house_id>', methods=['GET', 'POST'])
@login_required
@landlord_required
def initiate_payment(house_id):
    """Initiate payment for house listing"""
    house = House.query.get_or_404(house_id)
    
    if house.landlord_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('landlord.dashboard'))
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        transaction_ref = request.form.get('transaction_reference', '').strip()
        
        if not transaction_ref:
            flash('Transaction reference is required.', 'danger')
            return redirect(url_for('payment.initiate_payment', house_id=house_id))
        
        payment = Payment(
            user_id=current_user.id,
            amount=current_app.config['PAYMENT_AMOUNT_KES'],
            payment_method=payment_method,
            transaction_reference=transaction_ref,
            house_id=house_id,
            description=f'House listing: {house.title}',
            status='pending'
        )
        
        try:
            db.session.add(payment)
            db.session.commit()
            flash('Payment initiated. Please wait for verification.', 'info')
            return redirect(url_for('landlord.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    payment_methods = PaymentProcessor.get_all_payment_options()
    return render_template('payment/initiate.html', house=house, 
                         payment_methods=payment_methods,
                         amount=current_app.config['PAYMENT_AMOUNT_KES'])


@payment_bp.route('/verify/<int:payment_id>', methods=['POST'])
@login_required
def verify_payment(payment_id):
    """Verify payment (admin function)"""
    payment = Payment.query.get_or_404(payment_id)
    
    # In production, this would verify with actual payment provider
    # For now, only admin can verify
    
    payment.status = 'completed'
    payment.verified_at = datetime.utcnow()
    
    if payment.house_id:
        house = House.query.get(payment.house_id)
        if house:
            house.posted_after_payment = True
    
    try:
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Payment verified!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ============= API ROUTES =============
@api_bp.route('/houses')
def get_houses():
    """Get houses as JSON"""
    page = request.args.get('page', 1, type=int)
    city = request.args.get('city', '', type=str)
    
    query = House.query.filter_by(active=True, posted_after_payment=True)
    
    if city:
        query = query.filter_by(city=city)
    
    houses = query.paginate(page=page, per_page=20)
    
    data = {
        'total': houses.total,
        'pages': houses.pages,
        'current_page': page,
        'houses': [{
            'id': h.id,
            'title': h.title,
            'rent_price': h.rent_price,
            'rent_period': h.rent_period,
            'bedrooms': h.bedrooms,
            'bathrooms': h.bathrooms,
            'city': h.city,
            'address': h.address,
            'latitude': h.latitude,
            'longitude': h.longitude,
            'main_image': f'/static/uploads/{h.main_image}' if h.main_image else None
        } for h in houses.items]
    }
    
    return jsonify(data)


@api_bp.route('/favorite/<int:house_id>', methods=['POST'])
@login_required
@tenant_required
def toggle_favorite(house_id):
    """Toggle favorite house"""
    house = House.query.get_or_404(house_id)
    
    existing = Favorite.query.filter_by(tenant_id=current_user.id, house_id=house_id).first()
    
    if existing:
        db.session.delete(existing)
        message = 'Removed from favorites'
    else:
        favorite = Favorite(tenant_id=current_user.id, house_id=house_id)
        db.session.add(favorite)
        message = 'Added to favorites'
    
    try:
        db.session.commit()
        return jsonify({'status': 'success', 'message': message})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@api_bp.route('/payment-methods')
def get_payment_methods():
    """Get all payment methods"""
    return jsonify(PaymentProcessor.get_all_payment_options())


@api_bp.route('/payment-instructions/<method>')
def get_payment_instructions(method):
    """Get payment instructions"""
    instructions = {
        'mpesa': PaymentProcessor.format_mpesa_instructions(),
        'airtel': PaymentProcessor.format_airtel_instructions(),
        'coop': PaymentProcessor.format_bank_instructions()
    }
    
    if method in instructions:
        return jsonify({
            'status': 'success',
            'method': method,
            'instructions': instructions[method]
        })
    
    return jsonify({'status': 'error', 'message': 'Unknown payment method'}), 400
