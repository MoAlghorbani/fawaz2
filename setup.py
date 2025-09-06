#!/usr/bin/env python
"""
Setup script for Daily Equipment Inspection System
This script helps set up the project for development or production.
"""

import os
import sys
import subprocess
import argparse


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False


def setup_project(dev=False):
    """Set up the Django project."""
    print("🚀 Setting up Daily Equipment Inspection System")
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: You're not in a virtual environment. It's recommended to create one.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled. Please create and activate a virtual environment first.")
            return False
    
    # Install requirements
    requirements_file = "requirements-dev.txt" if dev else "requirements.txt"
    if not run_command(f"pip install -r {requirements_file}", f"Installing packages from {requirements_file}"):
        return False
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return False
    
    if not run_command("python manage.py migrate", "Applying migrations"):
        return False
    
    # Load initial data
    if not run_command("python manage.py load_checklist_items", "Loading initial checklist items"):
        return False
    
    # Collect static files (if in production mode)
    if not dev:
        run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Start the development server: python manage.py runserver")
    print("3. Access the admin interface: http://127.0.0.1:8000/admin/")
    print("4. Access the API: http://127.0.0.1:8000/api/")
    
    return True


def create_superuser():
    """Create a superuser interactively."""
    print("\n👤 Creating superuser...")
    try:
        subprocess.run("python manage.py createsuperuser", shell=True, check=True)
        print("✅ Superuser created successfully")
    except subprocess.CalledProcessError:
        print("❌ Error creating superuser")


def main():
    parser = argparse.ArgumentParser(description="Setup Daily Equipment Inspection System")
    parser.add_argument("--dev", action="store_true", help="Install development dependencies")
    parser.add_argument("--create-superuser", action="store_true", help="Create superuser after setup")
    
    args = parser.parse_args()
    
    if setup_project(dev=args.dev):
        if args.create_superuser:
            create_superuser()
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()