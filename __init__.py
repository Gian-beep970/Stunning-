"""Main Flask application for IMPERIAL HOUSE"""
import os
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
import json

from app.config import config
from app.models import db, User, House, HouseImage, Payment, Favorite, Message
from app.payments import PaymentProcessor
from app.utils import save_upload_file, delete_upload_file, ALLOWED_EXTENSIONS

login_manager = LoginManager()


def create_app(config_name='development'):
    """Create and configure Flask application"""
    app = Flask(__name__, instance_relative_config=False)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Create application context
    with app.app_context():
        # Register blueprints
        from app.routes import auth_bp, main_bp, landlord_bp, tenant_bp, payment_bp, api_bp
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)
        app.register_blueprint(landlord_bp)
        app.register_blueprint(tenant_bp)
        app.register_blueprint(payment_bp)
        app.register_blueprint(api_bp)
        
        # Create tables
        db.create_all()
        
        return app


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID"""
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    """Handle unauthorized access"""
    flash('You need to log in first.', 'danger')
    return redirect(url_for('auth.login'))
