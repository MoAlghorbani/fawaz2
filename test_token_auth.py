#!/usr/bin/env python
"""
Test script to demonstrate token-based authentication with the API
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_token_authentication():
    print("🔧 Testing Token-Based Authentication")
    print("=" * 50)
    
    # Step 1: Login to get token
    print("\n1. 🔐 Login to get authentication token")
    login_data = {
        "username": "admin", 
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login/",
            headers={"Content-Type": "application/json"},
            data=json.dumps(login_data)
        )
        
        if response.status_code == 200:
            login_result = response.json()
            token = login_result["token"]
            user = login_result["user"]
            
            print(f"✅ Login successful!")
            print(f"Token: {token}")
            print(f"User: {user['username']} (ID: {user['id']})")
            
            # Step 2: Test API access with token
            print("\n2. 🔍 Testing API access with token")
            
            headers = {
                "Authorization": f"Token {token}",
                "Content-Type": "application/json"
            }
            
            # Test equipment endpoint
            equipment_response = requests.get(
                f"{BASE_URL}/api/equipment/",
                headers=headers
            )
            
            if equipment_response.status_code == 200:
                equipment_data = equipment_response.json()
                print(f"✅ Equipment API access successful!")
                print(f"Found {equipment_data['count']} equipment items")
            else:
                print(f"❌ Equipment API access failed: {equipment_response.status_code}")
                print(equipment_response.text)
            
            # Test user info endpoint
            print("\n3. 👤 Testing user info endpoint")
            user_info_response = requests.get(
                f"{BASE_URL}/api/auth/user/",
                headers=headers
            )
            
            if user_info_response.status_code == 200:
                user_info = user_info_response.json()
                print(f"✅ User info retrieved successfully!")
                print(f"User: {user_info['user']['username']}")
            else:
                print(f"❌ User info failed: {user_info_response.status_code}")
            
            # Step 3: Test logout
            print("\n4. 🚪 Testing logout (token deletion)")
            logout_response = requests.post(
                f"{BASE_URL}/api/auth/logout/",
                headers=headers
            )
            
            if logout_response.status_code == 200:
                print(f"✅ Logout successful!")
                print("Token has been deleted")
                
                # Test API access after logout
                print("\n5. 🔒 Testing API access after logout")
                test_response = requests.get(
                    f"{BASE_URL}/api/equipment/",
                    headers=headers
                )
                
                if test_response.status_code == 401:
                    print(f"✅ API correctly denies access after logout")
                else:
                    print(f"❌ API still allows access after logout: {test_response.status_code}")
            else:
                print(f"❌ Logout failed: {logout_response.status_code}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure Django is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    test_token_authentication()