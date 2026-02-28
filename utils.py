"""Utility functions for IMPERIAL HOUSE"""
import os
from werkzeug.utils import secure_filename
from PIL import Image
import io

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload_file(file, upload_folder, prefix='house'):
    """Save uploaded file and return filename"""
    if not file or file.filename == '':
        return None
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to make unique
        import time
        filename = f"{prefix}_{int(time.time())}_{filename}"
        
        filepath = os.path.join(upload_folder, filename)
        
        # Create upload folder if it doesn't exist
        os.makedirs(upload_folder, exist_ok=True)
        
        # Optimize image before saving
        img = Image.open(file)
        img.thumbnail((1200, 1200))  # Max dimensions
        img.save(filepath, quality=85, optimize=True)
        
        return filename
    
    return None


def delete_upload_file(filename, upload_folder):
    """Delete uploaded file"""
    if filename:
        filepath = os.path.join(upload_folder, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    return False


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates (Haversine formula)"""
    from math import radians, cos, sin, asin, sqrt
    
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r


def format_currency(amount):
    """Format amount as KES currency"""
    return f"KES {amount:,.2f}"
