#!/usr/bin/env python
"""
Create initial admin account for Ifugao PPO BMI Monitor.

Usage:
    python create_admin.py
    
This script will:
1. Check if admin account already exists
2. Create admin user with must_change_password=True
3. Prompt for initial temporary password
4. Save credentials securely for first login
"""

import os
import sys
import django
from getpass import getpass

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmi_monitor.settings')
django.setup()

from api.models import CustomUser
from django.contrib.auth.hashers import make_password


def create_admin():
    """Create initial admin account."""
    
    print("\n" + "="*60)
    print("Ifugao PPO BMI Monitor - Admin Account Creation")
    print("="*60 + "\n")
    
    # Check if admin exists
    if CustomUser.objects.filter(is_staff=True, is_superuser=True, is_personnel=False).exists():
        print("⚠️  Admin account already exists!")
        print("To create additional admins, use: python manage.py createsuperuser")
        return
    
    # Get credentials
    print("Create the initial admin account.")
    print("This admin will be required to change password on first login.\n")
    
    username = input("Admin username (default: admin): ").strip() or "admin"
    
    # Check if username exists
    if CustomUser.objects.filter(username=username).exists():
        print(f"❌ Username '{username}' already exists!")
        return
    
    # Get temporary password
    print("\nSet a temporary password for initial login.")
    print("On first login, the admin will be forced to change it.")
    print("Password requirements:")
    print("  - Minimum 8 characters")
    print("  - Alphanumeric only (no special characters)")
    print("  - At least 1 uppercase letter")
    print("  - At least 2 lowercase letters")
    print("  - At least 1 digit")
    print("  Example: Pass1234\n")
    
    while True:
        password = getpass("Temporary password: ")
        if len(password) < 8:
            print("❌ Password too short (minimum 8 characters)")
            continue
        
        if not password.replace('_', '').isalnum():
            print("❌ Password contains invalid characters (alphanumeric only)")
            continue
        
        if not any(c.isupper() for c in password):
            print("❌ Password must contain at least 1 uppercase letter")
            continue
        
        if sum(c.islower() for c in password) < 2:
            print("❌ Password must contain at least 2 lowercase letters")
            continue
        
        if not any(c.isdigit() for c in password):
            print("❌ Password must contain at least 1 digit")
            continue
        
        confirm = getpass("Confirm password: ")
        if password != confirm:
            print("❌ Passwords don't match!")
            continue
        
        break
    
    # Create admin user
    try:
        admin = CustomUser.objects.create(
            username=username,
            email=f'{username}@ifugao-ppo.gov.ph',
            first_name='System',
            last_name='Administrator',
            is_staff=True,
            is_superuser=True,
            is_personnel=False,
            must_change_password=True,  # Force password change on first login
            rank='PBGEN',
            rank_classification='PCO',
            unit='PHQ',
        )
        admin.set_password(password)
        admin.save()
        
        print("\n" + "="*60)
        print("✅ Admin account created successfully!")
        print("="*60)
        print(f"\nUsername: {username}")
        print(f"Temporary Password: {password}")
        print("\n📝 IMPORTANT SECURITY NOTES:")
        print("1. On first login, admin will be required to change password")
        print("2. After password change, admin must scan QR code in Google Authenticator")
        print("3. Save these credentials securely")
        print("4. Share credentials with admin via secure channel (NOT email/Slack)\n")
        
        # Save credentials to secure file
        creds_file = f"admin_credentials_{username}.txt"
        with open(creds_file, 'w') as f:
            f.write(f"Ifugao PPO BMI Monitor - Admin Credentials\n")
            f.write(f"Created: {django.utils.timezone.now()}\n")
            f.write(f"Username: {username}\n")
            f.write(f"Temporary Password: {password}\n")
            f.write(f"\nIMPORTANT: Delete this file after sharing with admin!\n")
        
        print(f"💾 Credentials saved to: {creds_file}")
        print("   ⚠️  Delete this file after sharing with admin for security!\n")
        
    except Exception as e:
        print(f"\n❌ Error creating admin account: {e}\n")
        return


if __name__ == '__main__':
    try:
        create_admin()
    except KeyboardInterrupt:
        print("\n\nAborted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        sys.exit(1)
