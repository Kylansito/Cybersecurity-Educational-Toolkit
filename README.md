# Cybersecurity Educational Toolkit

⚠️ **EDUCATIONAL PURPOSES ONLY** ⚠️

> **Note:** This is an ongoing project that is being actively developed. More tools and educational resources will be added over time.

This repository contains cybersecurity demonstration tools designed exclusively for educational and training purposes. These tools simulate various cyber attacks to help security professionals, students, and educators understand attack vectors and develop effective defensive strategies.

## Disclaimer

All tools in this repository are provided strictly for:
- Educational demonstrations
- Security training
- Awareness programs
- Testing your own systems with proper authorization

**NEVER** use these tools against systems without explicit permission. Unauthorized use may violate local, state, and federal laws. The authors and contributors are not responsible for any misuse or damage caused by these tools.

## Repository Contents

### 1. Fake Hotspot (`fake-hotspot.py`)
A demonstration tool that simulates a malicious WiFi captive portal mimicking Google's login page. Shows how attackers can create convincing fake access points to harvest credentials.

**Features:**
- Simulates a Google-style login page
- Captures and logs submitted credentials
- Includes clear warning banners indicating it's a demo
- Instructor view for demonstration purposes

### 2. Brute Force (`brute-force.py`)
An educational demonstration of brute force password cracking techniques. Helps understand the importance of strong passwords and modern authentication protections.

**Features:**
- Supports various character sets (lowercase, uppercase, digits, symbols)
- Multiple attack methods (brute force and dictionary)
- Performance metrics display
- Support for various hash algorithms

### 3. Social Engineering (`social-engineering.py`)
A toolkit demonstrating Catalan-focused OSINT (Open Source Intelligence) gathering techniques and targeted phishing campaign generation. Illustrates how attackers craft region-specific attacks.

**Features:**
- OSINT collection for Catalan targets
- Phishing email template generation
- Multiple attack vector demonstrations
- Educational component explaining detection and prevention

### 4. CUPP Generator (`cupp-generator.py`)
Common User Passwords Profiler - A tool that generates potential password lists based on target information. Demonstrates how personal information can be used to crack passwords.

**Features:**
- Interactive information gathering
- Personalized password list generation
- Multiple variation techniques
- Leetspeak transformations

### 5. Phishing Website (`phishing-website.py`)
A Flask-based web application demonstrating a fake banking portal. Includes educational components explaining phishing techniques and protective measures.

**Features:**
- Realistic bank login simulation
- Educational follow-up page explaining phishing
- QR code generation for easy demo sharing
- Admin interface for demonstration purposes

## Installation Requirements

```bash
# Core dependencies
pip install flask requests bs4 colorama qrcode pillow

# Optional dependencies for specific tools
pip install argparse itertools hashlib datetime
```

## Usage Guidelines

1. **Always** run in controlled environments
2. **Never** deploy these on public networks without proper authorization
3. **Always** include the educational warning banners
4. Use as part of structured cybersecurity awareness training

## Educational Resources

For those using this toolkit in educational settings, consider supplementing with:
- OWASP Top 10 awareness documentation
- NIST cybersecurity framework
- Responsible disclosure policies
- Ethics in security testing discussions

## Project Status & Roadmap

This project is currently under active development. I am continually working to improve existing tools and add new demonstrations to create a more comprehensive educational toolkit. 

Planned future additions include:
- Network traffic analysis tools
- API security testing demonstrations
- Web application vulnerability scanners
- Secure coding practice examples
- More detailed defensive countermeasures

## Contributing

Contributions focused on improving the educational value and safety of these demonstrations are welcome. Please ensure any contributions:
- Maintain or enhance warning systems
- Include educational components
- Have clear documentation
- Are focused on learning, not exploitation

## License

These tools are provided for educational purposes only. Use responsibly.

---

*Remember that the best security professionals protect systems, not exploit them. Use these tools to learn, educate, and improve security posture.*
