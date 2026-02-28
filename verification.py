"""
Verification service for email and SMS notifications
Handles sending verification codes via email and SMS
"""
import random
import string
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from flask import current_app

class VerificationService:
    """Service for handling email and SMS verification"""
    
    @staticmethod
    def is_development():
        """Check if running in development mode"""
        try:
            # Check Flask debug mode
            if current_app.debug:
                return True
        except:
            pass
        
        # Check FLASK_ENV
        if os.environ.get('FLASK_ENV', 'development') == 'development':
            return True
        
        return False
    
    @staticmethod
    def generate_code(length=6):
        """Generate a random verification code"""
        return ''.join(random.choices(string.digits, k=length))
    
    @staticmethod
    def send_verification_email(email, code, user_name, user_type):
        """Send verification code via email"""
        try:
            subject = f"IMPERIAL HOUSE - Verify Your {user_type.title()} Account"
            
            # HTML email body
            html_body = f"""
            <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
                        .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 5px; }}
                        .header {{ background-color: #dc3545; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                        .header h1 {{ margin: 0; font-size: 28px; }}
                        .content {{ padding: 20px; text-align: center; }}
                        .code {{ font-size: 32px; font-weight: bold; color: #dc3545; letter-spacing: 5px; margin: 20px 0; }}
                        .footer {{ background-color: #f4f4f4; padding: 20px; text-align: center; font-size: 12px; color: #666; }}
                        .warning {{ color: #e74c3c; font-size: 12px; margin-top: 10px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1><i class="bi bi-house-fill"></i> IMPERIAL HOUSE</h1>
                            <p>Welcome to the Future of Rental Homes</p>
                        </div>
                        <div class="content">
                            <h2>Hello {user_name},</h2>
                            <p>Thank you for registering with IMPERIAL HOUSE as a {user_type.title()}!</p>
                            <p>Your verification code is:</p>
                            <div class="code">{code}</div>
                            <p>This code will expire in <strong>10 minutes</strong>.</p>
                            <p>If you did not create this account, please ignore this email.</p>
                            <div class="warning">
                                <strong>Never share this code with anyone.</strong> We will never ask you for this code.
                            </div>
                        </div>
                        <div class="footer">
                            <p>&copy; 2026 IMPERIAL HOUSE. All rights reserved.</p>
                            <p>This is an automated message. Please do not reply to this email.</p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            # Plain text fallback
            text_body = f"""
IMPERIAL HOUSE - Verify Your {user_type.title()} Account

Hello {user_name},

Thank you for registering with IMPERIAL HOUSE as a {user_type.title()}!

Your verification code is: {code}

This code will expire in 10 minutes.

If you did not create this account, please ignore this email.

Never share this code with anyone. We will never ask you for this code.

---
© 2026 IMPERIAL HOUSE. All rights reserved.
This is an automated message. Please do not reply to this email.
            """
            
            if VerificationService.is_development():
                # In development, print to console
                print(f"\n{'='*70}")
                print(f"📧 EMAIL VERIFICATION CODE FOR: {email}")
                print(f"{'='*70}")
                print(f"👤 User: {user_name} ({user_type})")
                print(f"📧 Email: {email}")
                print(f"🔐 CODE: {code}")
                print(f"⏱️  Expires: 10 minutes")
                print(f"{'='*70}\n")
                return True
            else:
                # In production, send actual email
                return VerificationService._send_smtp_email(
                    email, subject, text_body, html_body
                )
        except Exception as e:
            print(f"Error sending verification email: {str(e)}")
            return False
    
    @staticmethod
    def send_verification_sms(phone, code, user_name):
        """Send verification code via SMS"""
        try:
            if VerificationService.is_development():
                # In development, just print to console
                print(f"\n{'='*70}")
                print(f"📱 SMS VERIFICATION CODE FOR: {phone}")
                print(f"{'='*70}")
                print(f"👤 User: {user_name}")
                print(f"📱 Phone: {phone}")
                print(f"🔐 CODE: {code}")
                print(f"💬 Message: IMPERIAL HOUSE verification code: {code}")
                print(f"⏱️  Expires: 10 minutes")
                print(f"{'='*70}\n")
                return True
            else:
                # In production, use Twilio or similar service
                return VerificationService._send_twilio_sms(phone, code, user_name)
        except Exception as e:
            print(f"Error sending verification SMS: {str(e)}")
            return False
    
    @staticmethod
    @staticmethod
    def send_verification_whatsapp(phone, code, user_name):
        """Send verification code via WhatsApp"""
        try:
            if VerificationService.is_development():
                # In development, just print to console
                print(f"\n{'='*70}")
                print(f"💬 WHATSAPP VERIFICATION CODE FOR: {phone}")
                print(f"{'='*70}")
                print(f"👤 User: {user_name}")
                print(f"📱 Phone: {phone}")
                print(f"🔐 CODE: {code}")
                print(f"💬 Message: IMPERIAL HOUSE verification code: {code}")
                print(f"⏱️  Expires: 10 minutes")
                print(f"{'='*70}\n")
                return True
            else:
                # In production, use WhatsApp Business API
                return VerificationService._send_whatsapp_message(phone, code, user_name)
        except Exception as e:
            print(f"Error sending verification WhatsApp: {str(e)}")
            return False
    
    @staticmethod
    def _send_smtp_email(to_email, subject, text_body, html_body):
        """Send email via SMTP (production)"""
        try:
            smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.environ.get('SMTP_PORT', '587'))
            sender_email = os.environ.get('SENDER_EMAIL')
            sender_password = os.environ.get('SENDER_PASSWORD')
            
            if not sender_email or not sender_password:
                print("Warning: SMTP credentials not configured")
                return False
            
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = sender_email
            message['To'] = to_email
            
            # Attach parts
            message.attach(MIMEText(text_body, 'plain'))
            message.attach(MIMEText(html_body, 'html'))
            
            # Send
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, message.as_string())
            
            return True
        except Exception as e:
            print(f"SMTP Error: {str(e)}")
            return False
    
    @staticmethod
    def _send_twilio_sms(phone, code, user_name):
        """Send SMS via Twilio (production)"""
        try:
            # Import will only work if twilio is installed
            from twilio.rest import Client
            
            account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
            auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
            from_number = os.environ.get('TWILIO_PHONE_NUMBER')
            
            if not all([account_sid, auth_token, from_number]):
                print("Warning: Twilio credentials not configured")
                return False
            
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f"IMPERIAL HOUSE verification code: {code}. Valid for 10 minutes.",
                from_=from_number,
                to=phone
            )
            
            return True
        except ImportError:
            print("Warning: twilio package not installed")
            return False
        except Exception as e:
            print(f"Twilio Error: {str(e)}")
            return False
    
    @staticmethod
    def _send_whatsapp_message(phone, code, user_name):
        """Send WhatsApp message via WhatsApp Business API (production)"""
        try:
            # For now, use Twilio WhatsApp integration if available
            from twilio.rest import Client
            
            account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
            auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
            from_whatsapp = os.environ.get('TWILIO_WHATSAPP_NUMBER')
            
            if not all([account_sid, auth_token, from_whatsapp]):
                print("Warning: WhatsApp credentials not configured")
                return False
            
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f"IMPERIAL HOUSE verification code: {code}. Valid for 10 minutes.",
                from_=f"whatsapp:{from_whatsapp}",
                to=f"whatsapp:{phone}"
            )
            
            return True
        except ImportError:
            print("Warning: twilio package not installed")
            return False
        except Exception as e:
            print(f"WhatsApp Error: {str(e)}")
            return False


class CodeVerifier:
    """Verifies codes sent to users"""
    
    @staticmethod
    def verify_email_code(user, provided_code):
        """Verify email verification code"""
        if not user.email_verification_code:
            return False, "No verification code found"
        
        if user.email_verification_code != provided_code.strip():
            return False, "Invalid verification code"
        
        # Check if code expired (10 minutes)
        if user.verification_sent_at:
            expiry_time = user.verification_sent_at + timedelta(minutes=10)
            if datetime.utcnow() > expiry_time:
                return False, "Verification code expired"
        
        return True, "Email verified successfully"
    
    @staticmethod
    def verify_phone_code(user, provided_code):
        """Verify phone verification code"""
        if not user.phone_verification_code:
            return False, "No verification code found"
        
        if user.phone_verification_code != provided_code.strip():
            return False, "Invalid verification code"
        
        # Check if code expired (10 minutes)
        if user.verification_sent_at:
            expiry_time = user.verification_sent_at + timedelta(minutes=10)
            if datetime.utcnow() > expiry_time:
                return False, "Verification code expired"
        
        return True, "Phone verified successfully"
