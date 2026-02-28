from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for both landlords and tenants"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'landlord' or 'tenant'
    profile_picture = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    
    # Email/Phone verification fields
    is_email_verified = db.Column(db.Boolean, default=False)
    email_verification_code = db.Column(db.String(6), nullable=True)
    verification_method = db.Column(db.String(20), default='email')  # 'email', 'sms', 'whatsapp'
    phone_verified = db.Column(db.Boolean, default=False)
    phone_verification_code = db.Column(db.String(6), nullable=True)
    verification_sent_at = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    houses = db.relationship('House', backref='landlord', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='user', lazy=True, cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='tenant', lazy=True, cascade='all, delete-orphan')
    messages = db.relationship('Message', backref='sender', lazy=True, cascade='all, delete-orphan', foreign_keys='Message.sender_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class House(db.Model):
    """House listing model"""
    __tablename__ = 'houses'
    
    id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rent_price = db.Column(db.Float, nullable=False)
    rent_period = db.Column(db.String(20), nullable=False)  # 'monthly', 'yearly'
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    square_feet = db.Column(db.Float, nullable=True)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)  # For exact location
    longitude = db.Column(db.Float, nullable=False)  # For exact location
    amenities = db.Column(db.Text, nullable=True)  # JSON: wifi, parking, garden, etc.
    main_image = db.Column(db.String(255), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    posted_after_payment = db.Column(db.Boolean, default=False)  # Auto-posted after payment
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    images = db.relationship('HouseImage', backref='house', lazy=True, cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='house', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<House {self.title}>'


class HouseImage(db.Model):
    """House images model"""
    __tablename__ = 'house_images'
    
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<HouseImage {self.id}>'


class Payment(db.Model):
    """Payment transactions"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # 'mpesa', 'airtel', 'coop'
    transaction_reference = db.Column(db.String(100), nullable=True, unique=True)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'completed', 'failed'
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Payment {self.transaction_reference}>'


class Favorite(db.Model):
    """Tenant's favorite houses"""
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('tenant_id', 'house_id', name='unique_favorite'),)
    
    def __repr__(self):
        return f'<Favorite {self.tenant_id}-{self.house_id}>'


class Message(db.Model):
    """Direct messaging between landlords and tenants"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'), nullable=True)
    subject = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Message {self.id}>'
