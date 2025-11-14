#!/usr/bin/env python3
#
# Copyright (C) 2025 pdnguyen of HCMC University of Technology VNU-HCM.
# All rights reserved.
# This file is part of the CO3093/CO3094 course,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#
# WeApRous release - Client for Testing Task 1A & 1B
#

"""
client.py
~~~~~~~~~

Python client to test the WeApRous backend server (Task 1A & 1B).

Usage:
    python client.py                    (interactive menu)
    python client.py --login            (test login flow)
    python client.py --test-all         (run all tests)

This client:
    1. Sends HTTP requests to the backend
    2. Stores cookies from Set-Cookie headers
    3. Sends cookies in subsequent requests
    4. Displays responses and validates results
"""

import requests
import json
import argparse
from urllib.parse import urljoin

# Configuration
SERVER_URL = "http://localhost:9000"
CREDENTIALS = {
    "username": "admin",
    "password": "password"
}

class TestClient:
    """HTTP Client for testing WeApRous backend."""
    
    def __init__(self, server_url=SERVER_URL):
        self.server_url = server_url
        self.session = requests.Session()  # Auto-handles cookies!
        self.last_response = None
    
    def test_get_index_no_auth(self):
        """Test 1: GET / without authentication (should fail)."""
        print("\n" + "="*70)
        print("Test 1: GET / WITHOUT authentication")
        print("="*70)
        
        url = urljoin(self.server_url, "/")
        
        try:
            # Clear cookies to ensure no auth
            self.session.cookies.clear()
            
            response = self.session.get(url)
            self.last_response = response
            
            print(f"URL: {url}")
            print(f"Method: GET")
            print(f"Cookies sent: {dict(self.session.cookies)}")
            print(f"\nResponse:")
            print(f"  Status: {response.status_code} {response.reason}")
            print(f"  Headers: {dict(response.headers)}")
            print(f"  Body: {response.text}")
            
            # Validate
            expected = 401
            if response.status_code == expected:
                print(f"\n✅ PASS: Got expected status {expected}")
                return True
            else:
                print(f"\n❌ FAIL: Expected {expected}, got {response.status_code}")
                return False
        
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    def test_login(self):
        """Test 2: POST /login with valid credentials."""
        print("\n" + "="*70)
        print("Test 2: POST /login with valid credentials")
        print("="*70)
        
        url = urljoin(self.server_url, "/login")
        
        try:
            response = self.session.post(
                url,
                json=CREDENTIALS,
                headers={"Content-Type": "application/json"}
            )
            self.last_response = response
            
            print(f"URL: {url}")
            print(f"Method: POST")
            print(f"Body: {json.dumps(CREDENTIALS)}")
            print(f"\nResponse:")
            print(f"  Status: {response.status_code} {response.reason}")
            print(f"  Headers: {dict(response.headers)}")
            print(f"  Body: {response.text}")
            print(f"\nCookies received:")
            for key, value in self.session.cookies.items():
                print(f"  {key} = {value}")
            
            # Validate
            expected = 200
            if response.status_code == expected:
                print(f"\n✅ PASS: Got expected status {expected}")
                print(f"✅ Cookies stored: {dict(self.session.cookies)}")
                return True
            else:
                print(f"\n❌ FAIL: Expected {expected}, got {response.status_code}")
                return False
        
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    def test_get_index_with_auth(self):
        """Test 3: GET / with authentication (should succeed)."""
        print("\n" + "="*70)
        print("Test 3: GET / WITH authentication")
        print("="*70)
        
        url = urljoin(self.server_url, "/")
        
        try:
            response = self.session.get(url)
            self.last_response = response
            
            print(f"URL: {url}")
            print(f"Method: GET")
            print(f"Cookies sent: {dict(self.session.cookies)}")
            print(f"\nResponse:")
            print(f"  Status: {response.status_code} {response.reason}")
            print(f"  Headers: {dict(response.headers)}")
            print(f"  Body: {response.text}")
            
            # Validate
            expected = 200
            if response.status_code == expected:
                print(f"\n✅ PASS: Got expected status {expected}")
                return True
            else:
                print(f"\n❌ FAIL: Expected {expected}, got {response.status_code}")
                return False
        
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    def test_login_invalid(self):
        """Test 4: POST /login with invalid credentials."""
        print("\n" + "="*70)
        print("Test 4: POST /login with INVALID credentials")
        print("="*70)
        
        url = urljoin(self.server_url, "/login")
        invalid_creds = {"username": "hacker", "password": "wrong"}
        
        try:
            # Use new session without cookies
            temp_session = requests.Session()
            response = temp_session.post(
                url,
                json=invalid_creds,
                headers={"Content-Type": "application/json"}
            )
            self.last_response = response
            
            print(f"URL: {url}")
            print(f"Method: POST")
            print(f"Body: {json.dumps(invalid_creds)}")
            print(f"\nResponse:")
            print(f"  Status: {response.status_code} {response.reason}")
            print(f"  Body: {response.text}")
            
            # Validate
            expected = 401
            if response.status_code == expected:
                print(f"\n✅ PASS: Got expected status {expected}")
                return True
            else:
                print(f"\n❌ FAIL: Expected {expected}, got {response.status_code}")
                return False
        
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    def test_get_index_invalid_cookie(self):
        """Test 5: GET / with invalid cookie."""
        print("\n" + "="*70)
        print("Test 5: GET / with INVALID cookie")
        print("="*70)
        
        url = urljoin(self.server_url, "/")
        
        try:
            # Use new session and manually set invalid cookie
            temp_session = requests.Session()
            temp_session.cookies.set('auth', 'false')
            temp_session.cookies.set('sessionid', 'invalid123')
            
            response = temp_session.get(url)
            self.last_response = response
            
            print(f"URL: {url}")
            print(f"Method: GET")
            print(f"Cookies sent: {dict(temp_session.cookies)}")
            print(f"\nResponse:")
            print(f"  Status: {response.status_code} {response.reason}")
            print(f"  Body: {response.text}")
            
            # Validate
            expected = 401
            if response.status_code == expected:
                print(f"\n✅ PASS: Got expected status {expected}")
                return True
            else:
                print(f"\n❌ FAIL: Expected {expected}, got {response.status_code}")
                return False
        
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests in sequence."""
        print("\n" + "="*70)
        print("RUNNING ALL TESTS")
        print("="*70)
        
        results = []
        
        # Test 1: No auth
        results.append(("Test 1: GET / without auth", self.test_get_index_no_auth()))
        
        # Test 2: Login
        results.append(("Test 2: POST /login valid", self.test_login()))
        
        # Test 3: With auth
        results.append(("Test 3: GET / with auth", self.test_get_index_with_auth()))
        
        # Test 4: Invalid login
        results.append(("Test 4: POST /login invalid", self.test_login_invalid()))
        
        # Test 5: Invalid cookie
        results.append(("Test 5: GET / invalid cookie", self.test_get_index_invalid_cookie()))
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        passed = 0
        failed = 0
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status}: {test_name}")
            if result:
                passed += 1
            else:
                failed += 1
        
        print(f"\nTotal: {passed} passed, {failed} failed")
        
        return failed == 0
    
    def interactive_menu(self):
        """Interactive menu for manual testing."""
        while True:
            print("\n" + "="*70)
            print("WeApRous Client - Interactive Menu")
            print("="*70)
            print("1. GET / (no auth)")
            print("2. POST /login (valid credentials)")
            print("3. GET / (with auth)")
            print("4. POST /login (invalid credentials)")
            print("5. GET / (invalid cookie)")
            print("6. Run all tests")
            print("7. Custom request")
            print("0. Exit")
            print("="*70)
            
            choice = input("Select option: ").strip()
            
            if choice == '1':
                self.test_get_index_no_auth()
            elif choice == '2':
                self.test_login()
            elif choice == '3':
                self.test_get_index_with_auth()
            elif choice == '4':
                self.test_login_invalid()
            elif choice == '5':
                self.test_get_index_invalid_cookie()
            elif choice == '6':
                self.run_all_tests()
            elif choice == '7':
                self.custom_request()
            elif choice == '0':
                print("Exiting...")
                break
            else:
                print("❌ Invalid option")
    
    def custom_request(self):
        """Send custom HTTP request."""
        print("\n" + "="*70)
        print("Custom Request")
        print("="*70)
        
        method = input("Method (GET/POST): ").strip().upper()
        path = input("Path (e.g., /login): ").strip()
        body_input = input("Body (JSON, leave empty for none): ").strip()
        
        url = urljoin(self.server_url, path)
        
        try:
            if method == "GET":
                response = self.session.get(url)
            elif method == "POST":
                body = json.loads(body_input) if body_input else {}
                response = self.session.post(url, json=body)
            else:
                print("❌ Invalid method")
                return
            
            print(f"\nResponse:")
            print(f"  Status: {response.status_code}")
            print(f"  Body: {response.text}")
            print(f"  Cookies: {dict(self.session.cookies)}")
        
        except Exception as e:
            print(f"❌ ERROR: {e}")


def main():
    parser = argparse.ArgumentParser(description="WeApRous Client for Testing")
    parser.add_argument('--server-ip', default='localhost', help='Server IP')
    parser.add_argument('--server-port', type=int, default=9000, help='Server port')
    parser.add_argument('--login', action='store_true', help='Test login flow')
    parser.add_argument('--test-all', action='store_true', help='Run all tests')
    
    args = parser.parse_args()
    
    server_url = f"http://{args.server_ip}:{args.server_port}"
    client = TestClient(server_url)
    
    print(f"\n{'='*70}")
    print(f"WeApRous Client - Connected to {server_url}")
    print(f"{'='*70}")
    
    try:
        if args.test_all:
            client.run_all_tests()
        elif args.login:
            client.test_login()
            client.test_get_index_with_auth()
        else:
            client.interactive_menu()
    
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
