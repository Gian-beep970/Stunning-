#!/usr/bin/env python3
"""
IMPERIAL HOUSE - Automated Deployment Helper
Prepares app for deployment and provides Render configuration
"""

import os
import sys
import json
import secrets
from pathlib import Path

def check_prerequisites():
    """Check if all necessary files exist"""
    required_files = [
        'run.py',
        'requirements.txt',
        'app/__init__.py',
        'app/models.py',
        'app/routes.py',
        'app/config.py'
    ]
    
    print("\n" + "="*50)
    print("  IMPERIAL HOUSE - Deployment Helper")
    print("="*50 + "\n")
    
    print("[1/5] Checking project files...")
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
            print(f"  ✗ Missing: {file}")
        else:
            print(f"  ✓ Found: {file}")
    
    if missing:
        print(f"\n❌ ERROR: {len(missing)} files missing!")
        sys.exit(1)
    
    print("  ✓ All files present!\n")
    return True

def generate_secret_key():
    """Generate a secure SECRET_KEY for production"""
    print("[2/5] Generating secure SECRET_KEY...")
    key = secrets.token_urlsafe(32)
    print(f"  ✓ Generated: {key}\n")
    return key

def create_deployment_config(secret_key):
    """Create deployment configuration file"""
    print("[3/5] Creating deployment configuration...")
    
    config = {
        "app_name": "imperial-house",
        "region": "frankfurt",
        "runtime": "Python 3.11",
        "build_command": "pip install -r requirements.txt && python run.py init_db",
        "start_command": "gunicorn -w 4 -b 0.0.0.0:$PORT run:app",
        "environment_variables": {
            "FLASK_ENV": "production",
            "SECRET_KEY": secret_key,
        },
        "deployment_options": [
            {
                "platform": "Render",
                "region": "Frankfurt (fastest to Kenya)",
                "cost": "Free tier available",
                "url": "https://render.com"
            },
            {
                "platform": "PythonAnywhere",
                "region": "UK (fast to Kenya)",
                "cost": "Free tier available",
                "url": "https://pythonanywhere.com"
            },
            {
                "platform": "Railway",
                "region": "Global CDN",
                "cost": "Pay-as-you-go",
                "url": "https://railway.app"
            }
        ]
    }
    
    config_file = 'deployment-config.json'
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"  ✓ Config saved to: {config_file}\n")
    return config

def check_git():
    """Check if git is installed"""
    print("[4/5] Checking Git installation...")
    try:
        os.system('git --version > nul 2>&1')
        print("  ✓ Git is installed!\n")
        return True
    except:
        print("  ✗ Git not found.")
        print("  📥 Download from: https://git-scm.com/download/win\n")
        return False

def show_deployment_steps():
    """Display deployment steps"""
    print("[5/5] Next steps for deployment...\n")
    
    print("="*60)
    print("  DEPLOYMENT STEPS")
    print("="*60 + "\n")
    
    print("STEP 1: Create GitHub Account (Free)")
    print("-" * 40)
    print("  1. Visit: https://github.com/signup")
    print("  2. Create account")
    print("  3. Verify email\n")
    
    print("STEP 2: Create GitHub Repository")
    print("-" * 40)
    print("  1. Click '+' icon at top right")
    print("  2. Select 'New repository'")
    print("  3. Name: 'imperial-house'")
    print("  4. Click 'Create repository'\n")
    
    print("STEP 3: Push Code to GitHub")
    print("-" * 40)
    print("  Run these commands in Terminal/PowerShell:\n")
    print("  git init")
    print("  git add .")
    print("  git commit -m 'Initial commit: IMPERIAL HOUSE'")
    print("  git remote add origin https://github.com/YOUR_USERNAME/imperial-house.git")
    print("  git branch -M main")
    print("  git push -u origin main\n")
    
    print("STEP 4: Deploy to Render (Recommended - 5 minutes)")
    print("-" * 40)
    print("  1. Visit: https://render.com")
    print("  2. Sign up with GitHub")
    print("  3. Click 'New +' > 'Web Service'")
    print("  4. Connect GitHub repository")
    print("  5. Fill in settings (see deployment-config.json)")
    print("  6. Set environment variables:")
    print("     - FLASK_ENV = production")
    print("     - SECRET_KEY = (see deployment-config.json)")
    print("  7. Click 'Create Web Service'")
    print("  8. Wait 2-3 minutes for deployment")
    print("  9. Get live URL! 🎉\n")
    
    print("STEP 5: Test on Mobile")
    print("-" * 40)
    print("  1. Copy Render URL from dashboard")
    print("  2. Visit on mobile phone (any Kenya network)")
    print("  3. Test all features\n")
    
    print("="*60)
    print("  That's it! Your app will be live and accessible")
    print("  from any phone in Kenya!")
    print("="*60 + "\n")

def main():
    """Main deployment helper"""
    try:
        # Check all prerequisites
        check_prerequisites()
        
        # Generate secret key
        secret_key = generate_secret_key()
        
        # Create deployment config
        config = create_deployment_config(secret_key)
        
        # Check git
        git_installed = check_git()
        
        # Show deployment steps
        show_deployment_steps()
        
        print("\n📄 Configuration saved to: deployment-config.json")
        print("📖 Detailed guides available:")
        print("   - QUICK_DEPLOY.md (Fast version)")
        print("   - DEPLOY_TO_RENDER.md (Complete guide)\n")
        
        print("✅ Everything is ready for deployment!")
        print("📱 Start with: https://render.com\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
