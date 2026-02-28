"""Payment processing for IMPERIAL HOUSE"""
import json
from datetime import datetime

class PaymentProcessor:
    """Handle payment integration with M-PESA, Airtel Money, and CO-OP Bank"""
    
    # Your payment details
    PAYMENT_DETAILS = {
        'mpesa': {
            'number': '0718357417',
            'name': 'M-PESA'
        },
        'airtel': {
            'number': '0103633071',
            'name': 'Airtel Money'
        },
        'coop': {
            'account_number': '01102672539001',
            'paybill': '400200',
            'name': 'CO-OP Bank'
        }
    }
    
    AMOUNT_KES = 5000
    
    @staticmethod
    def get_payment_details(payment_method):
        """Get payment details for a specific method"""
        return PaymentProcessor.PAYMENT_DETAILS.get(payment_method, {})
    
    @staticmethod
    def generate_payment_reference(user_id, house_id=None):
        """Generate unique payment reference"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        ref = f"IH{user_id}{house_id or 0}{timestamp}"
        return ref
    
    @staticmethod
    def format_mpesa_instructions():
        """Format M-PESA payment instructions"""
        details = PaymentProcessor.PAYMENT_DETAILS['mpesa']
        return f"""
        M-PESA Payment Instructions:
        1. Go to your M-PESA menu
        2. Select 'Send Money'
        3. Enter Phone Number: {details['number']}
        4. Enter Amount: KES {PaymentProcessor.AMOUNT_KES}
        5. Complete the transaction
        6. Copy the transaction reference (e.g., DQC2XXXXXXX)
        7. Paste it above and click 'Verify Payment'
        
        Contact: {details['number']}
        """
    
    @staticmethod
    def format_airtel_instructions():
        """Format Airtel Money payment instructions"""
        details = PaymentProcessor.PAYMENT_DETAILS['airtel']
        return f"""
        Airtel Money Payment Instructions:
        1. Go to your Airtel Money menu
        2. Select 'Send Money'
        3. Enter Airtel Number: {details['number']}
        4. Enter Amount: KES {PaymentProcessor.AMOUNT_KES}
        5. Complete the transaction
        6. Copy the transaction reference
        7. Paste it above and click 'Verify Payment'
        
        Contact: {details['number']}
        """
    
    @staticmethod
    def format_bank_instructions():
        """Format CO-OP Bank payment instructions"""
        details = PaymentProcessor.PAYMENT_DETAILS['coop']
        return f"""
        CO-OP Bank Payment Instructions:
        1. Visit any CO-OP Bank branch or use online banking
        2. Make payment to:
           - Account Number: {details['account_number']}
           - Paybill Number: {details['paybill']}
        3. Amount: KES {PaymentProcessor.AMOUNT_KES}
        4. Include transaction reference in description
        5. Get confirmation receipt
        6. Paste the reference above and click 'Verify Payment'
        
        Account Details:
        - Account: {details['account_number']}
        - Paybill: {details['paybill']}
        """
    
    @staticmethod
    def verify_payment(reference, amount, payment_method):
        """
        Verify payment - In production, this would call actual payment APIs
        For now, returns instruction for manual verification
        """
        return {
            'status': 'pending_verification',
            'reference': reference,
            'amount': amount,
            'method': payment_method,
            'message': 'Payment verification pending. Admin will verify within 24 hours.'
        }
    
    @staticmethod
    def get_all_payment_options():
        """Get all available payment options"""
        return {
            'mpesa': {
                'name': 'M-PESA',
                'number': PaymentProcessor.PAYMENT_DETAILS['mpesa']['number'],
                'type': 'mobile_money'
            },
            'airtel': {
                'name': 'Airtel Money',
                'number': PaymentProcessor.PAYMENT_DETAILS['airtel']['number'],
                'type': 'mobile_money'
            },
            'coop': {
                'name': 'CO-OP Bank',
                'paybill': PaymentProcessor.PAYMENT_DETAILS['coop']['paybill'],
                'account': PaymentProcessor.PAYMENT_DETAILS['coop']['account_number'],
                'type': 'bank'
            }
        }
