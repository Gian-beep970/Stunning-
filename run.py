#!/usr/bin/env python
"""
IMPERIAL HOUSE - Rental Property Listing Application
Main application entry point
"""

import os
from app import create_app
from app.models import db

# Create Flask application
app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Add objects to the Flask shell"""
    return {'db': db}

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('Database initialized!')

@app.cli.command()
def create_sample_data():
    """Create sample data for testing"""
    from app.models import User, House
    
    # Create sample landlord
    landlord = User(
        username='landlord1',
        email='landlord1@imperial.house',
        phone='0718357417',
        full_name='John Landlord',
        user_type='landlord'
    )
    landlord.set_password('password123')
    
    # Create sample tenant
    tenant = User(
        username='tenant1',
        email='tenant1@imperial.house',
        phone='0700000001',
        full_name='Jane Tenant',
        user_type='tenant'
    )
    tenant.set_password('password123')
    
    try:
        db.session.add(landlord)
        db.session.add(tenant)
        db.session.commit()
        print('Sample users created!')
        print('Landlord: landlord1 / password123')
        print('Tenant: tenant1 / password123')
    except Exception as e:
        db.session.rollback()
        print(f'Error creating sample data: {e}')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
