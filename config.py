import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///imperialhouse.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'imperial-house-dev-secret-key-change-in-production'
    
    # Upload settings
    UPLOAD_FOLDER = 'app/static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Payment settings
    PAYMENT_AMOUNT_KES = 5000
    
    # M-PESA Configuration
    MPESA_NUMBER = '0718357417'
    
    # Airtel Money Configuration
    AIRTEL_NUMBER = '0103633071'
    
    # CO-OP Bank Configuration
    COOP_ACCOUNT = '01102672539001'
    COOP_PAYBILL = '400200'
    
    # Google Maps API Key (set in environment)
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY') or ''
    
    # Kenya Cities and Towns List (alphabetically organized)
    KENYA_CITIES = [
        # Major Cities (Central)
        'Nairobi',
        'Nakuru',
        'Kericho',
        'Kisii',
        
        # Coastal Region
        'Mombasa',
        'Malindi',
        'Lamu',
        'Kilifi',
        'Diani',
        'Mtwapa',
        
        # Western Region
        'Kisumu',
        'Kisi',
        'Bungoma',
        'Kakamega',
        'Kitale',
        
        # Rift Valley
        'Eldoret',
        'Naivasha',
        'Kericho',
        'Nandi Hills',
        'Uasin Gishu',
        
        # North Eastern
        'Isiolo',
        'Nyeri',
        'Nanyuki',
        'Murang\'a',
        'Embu',
        'Meru',
        'Tharaka Nithi',
        'Kirinyaga',
        
        # North
        'Lamu',
        'Garissa',
        'Wajir',
        'Mandera',
        
        # Eastern
        'Nairobi East',
        'Limuru',
        'Kajiado',
        'Machakos',
        'Kilimani',
        'Athi River',
        'Makueni',
        'Bungoma',
        
        # Additional Towns
        'Ngong',
        'Ongata Rongai',
        'Runda',
        'Westlands',
        'Upper Hill',
        'Kilimani',
        'Lavington',
        'Riverside',
        'Motomoto',
        'South C',
        'South B',
        'Huruma',
        'Eastleigh',
        'Embakasi',
        'Viwandani',
        'Mathare',
        'Kahawa',
        'Thika',
        'Ruiru',
        'Murang\'a',
        'Nyeri',
        'Karatina',
        'Iten',
        'Kapsabet',
        'Eldume',
        'Bomet',
        'Sotik',
        'Kipchoge',
        'Molo',
        'Londiani',
        'Mogotio',
        'Rumuruti',
        'Laikipia',
        'Archers Post',
        'Timau',
        'Maralal',
        'Barsaloi',
        'Samburu',
        'Mkurumadzi',
        'Mwingi',
        'Kitui',
        'Mutomo',
        'Wote',
        'Voi',
        'Taveta',
        'Vol',
        'Mtito Andei',
        'Kibwezi',
        'Mariakani',
        'Moshi',
        'Ukunda',
        'Lunga Lunga',
        'Ramisi',
        'Moshi',
        'Nyali',
        'Mtwapa',
        'Bamburi',
        'Shanzu',
        'Jomvu',
        'Likoni',
        'Msingi',
        'Mbezi',
        'Tanga',
        'Pemba',
        'Kiunga',
        'Witu',
        'Pate',
        'Manda',
        'Siyu',
        'Faza',
        'Mpeketoni',
        'Muanda',
        'Mokowe',
        'Kipini',
        'Amu',
        'Kizingitini',
        'Matondoni',
        'Mwembe',
        'Whydah',
        'Manda',
        'Siu',
        'Pate',
        'Faza',
    ]


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
