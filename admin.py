"""
IMPERIAL HOUSE - Admin Management Utilities
For future admin panel integration
"""

from app.models import db, Payment, House, User

def verify_payment(payment_id):
    """Verify a pending payment"""
    payment = Payment.query.get(payment_id)
    if not payment:
        return False
    
    payment.status = 'completed'
    
    # Auto-publish house after payment
    if payment.house_id:
        house = House.query.get(payment.house_id)
        if house:
            house.posted_after_payment = True
            house.active = True
    
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False

def reject_payment(payment_id, reason=''):
    """Reject a payment"""
    payment = Payment.query.get(payment_id)
    if not payment:
        return False
    
    payment.status = 'failed'
    
    try:
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False

def get_pending_payments():
    """Get all pending payments"""
    return Payment.query.filter_by(status='pending').all()

def get_landlord_stats():
    """Get general landlord statistics"""
    total_landlords = User.query.filter_by(user_type='landlord').count()
    total_houses = House.query.count()
    active_houses = House.query.filter_by(active=True).count()
    total_payments = Payment.query.filter_by(status='completed').count()
    
    return {
        'total_landlords': total_landlords,
        'total_houses': total_houses,
        'active_houses': active_houses,
        'total_payments': total_payments,
        'total_revenue': total_payments * 5000  # KES 5000 per listing
    }

def get_tenant_stats():
    """Get tenant statistics"""
    total_tenants = User.query.filter_by(user_type='tenant').count()
    return {'total_tenants': total_tenants}
