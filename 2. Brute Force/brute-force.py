#!/usr/bin/env python3
"""
Brute Force Password Cracker - Educational Demo
For cybersecurity education purposes only
"""

import string
import time
import argparse
import itertools
import hashlib
import os
from getpass import getpass

class BruteForceDemo:
    def __init__(self):
        self.start_time = None
        self.attempts = 0
        self.password_found = False
        self.charset = None
    
    def set_charset(self, use_lowercase=True, use_uppercase=False, use_digits=False, use_symbols=False):
        """Define the character set to use for brute forcing"""
        self.charset = ""
        if use_lowercase:
            self.charset += string.ascii_lowercase
        if use_uppercase:
            self.charset += string.ascii_uppercase
        if use_digits:
            self.charset += string.digits
        if use_symbols:
            self.charset += string.punctuation
            
        if not self.charset:
            # Default to lowercase if nothing selected
            self.charset = string.ascii_lowercase
            
        print(f"Using character set ({len(self.charset)} chars): {self.charset}")
    
    def hash_password(self, password, algorithm='sha256'):
        """Create a hash of the password using the specified algorithm"""
        if algorithm == 'md5':
            return hashlib.md5(password.encode()).hexdigest()
        elif algorithm == 'sha1':
            return hashlib.sha1(password.encode()).hexdigest()
        else:  # default to sha256
            return hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, attempt, target_password, hash_mode=False, hash_algorithm='sha256'):
        """Check if the password attempt is correct"""
        self.attempts += 1
        
        # Display progress every 1000 attempts
        if self.attempts % 1000 == 0:
            elapsed = time.time() - self.start_time
            rate = self.attempts/elapsed if elapsed > 0 else 0
            print(f"Attempts: {self.attempts}, Current: {attempt}, Time: {elapsed:.2f}s, Rate: {rate:.2f}/s")
        
        if hash_mode:
            hashed_attempt = self.hash_password(attempt, hash_algorithm)
            return hashed_attempt == target_password
        else:
            return attempt == target_password
    
    def brute_force(self, target_password, max_length=4, hash_mode=False, hash_algorithm='sha256'):
        """Perform a brute force attack on the target password"""
        print(f"Starting brute force attack (max length: {max_length})")
        print("Press Ctrl+C to stop the attack at any time")
        
        self.start_time = time.time()
        self.attempts = 0
        self.password_found = False
        
        for length in range(1, max_length + 1):
            print(f"\nTrying passwords of length {length}...")
            for attempt in itertools.product(self.charset, repeat=length):
                password_attempt = ''.join(attempt)
                
                if self.check_password(password_attempt, target_password, hash_mode, hash_algorithm):
                    self.password_found = True
                    elapsed = time.time() - self.start_time
                    print(f"\n[SUCCESS] Password found: '{password_attempt}'")
                    print(f"Attempts: {self.attempts}")
                    print(f"Time elapsed: {elapsed:.2f} seconds")
                    rate = self.attempts/elapsed if elapsed > 0 else 0
                    print(f"Attempt rate: {rate:.2f} passwords/second")
                    return password_attempt
        
        elapsed = time.time() - self.start_time
        print("\n[FAILED] Password not found within the specified parameters")
        print(f"Attempts: {self.attempts}")
        print(f"Time elapsed: {elapsed:.2f} seconds")
        rate = self.attempts/elapsed if elapsed > 0 else 0
        print(f"Attempt rate: {rate:.2f} passwords/second")
        return None
        
    def dictionary_attack(self, target_password, wordlist_path, hash_mode=False, hash_algorithm='sha256'):
        """Perform a dictionary attack using a wordlist"""
        if not os.path.exists(wordlist_path):
            print(f"[ERROR] Wordlist file not found: {wordlist_path}")
            return None
            
        print(f"Starting dictionary attack using wordlist: {wordlist_path}")
        print("Press Ctrl+C to stop the attack at any time")
        
        self.start_time = time.time()
        self.attempts = 0
        self.password_found = False
        
        try:
            # Get file size for progress reporting
            file_size = os.path.getsize(wordlist_path)
            print(f"Wordlist size: {file_size/1024/1024:.2f} MB")
            
            with open(wordlist_path, 'r', errors='ignore') as wordlist:
                for line in wordlist:
                    password_attempt = line.strip()
                    
                    if self.check_password(password_attempt, target_password, hash_mode, hash_algorithm):
                        self.password_found = True
                        elapsed = time.time() - self.start_time
                        print(f"\n[SUCCESS] Password found: '{password_attempt}'")
                        print(f"Attempts: {self.attempts}")
                        print(f"Time elapsed: {elapsed:.2f} seconds")
                        rate = self.attempts/elapsed if elapsed > 0 else 0
                        print(f"Attempt rate: {rate:.2f} passwords/second")
                        return password_attempt
                        
        except UnicodeDecodeError as e:
            # Handle encoding errors in the wordlist
            print(f"\n[WARNING] Encoding issue in wordlist at attempt {self.attempts}: {e}")
            print("Continuing with the rest of the wordlist...")
            
        elapsed = time.time() - self.start_time
        print("\n[FAILED] Password not found in wordlist")
        print(f"Attempts: {self.attempts}")
        print(f"Time elapsed: {elapsed:.2f} seconds")
        rate = self.attempts/elapsed if elapsed > 0 else 0
        print(f"Attempt rate: {rate:.2f} passwords/second")
        return None
        
def main():
    parser = argparse.ArgumentParser(description="Brute Force Password Cracker - Educational Demo")
    
    # Target options
    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument("-p", "--password", help="Target password to crack")
    target_group.add_argument("-i", "--interactive", action="store_true", help="Input password interactively (hidden)")
    target_group.add_argument("-H", "--hash", help="Target password hash to crack")
    
    # Attack type options
    attack_group = parser.add_mutually_exclusive_group()
    attack_group.add_argument("-b", "--brute-force", action="store_true", default=True, 
                            help="Use brute force attack (default)")
    attack_group.add_argument("-w", "--wordlist", 
                            help="Use dictionary attack with the specified wordlist file (e.g., rockyou.txt)")
    
    # Character set options (for brute force)
    charset_group = parser.add_argument_group("Character Set Options (for brute force)")
    charset_group.add_argument("-l", "--lowercase", action="store_true", help="Use lowercase letters (a-z)")
    charset_group.add_argument("-u", "--uppercase", action="store_true", help="Use uppercase letters (A-Z)")
    charset_group.add_argument("-d", "--digits", action="store_true", help="Use digits (0-9)")
    charset_group.add_argument("-s", "--symbols", action="store_true", help="Use special symbols (!@#$, etc.)")
    
    # Attack parameters
    parser.add_argument("-m", "--max-length", type=int, default=4, help="Maximum password length to try (default: 4)")
    parser.add_argument("-a", "--algorithm", choices=["md5", "sha1", "sha256"], default="sha256", 
                        help="Hash algorithm to use when hash mode is enabled (default: sha256)")
    
    args = parser.parse_args()
    
    # Get the target password
    target_password = None
    hash_mode = False
    
    if args.password:
        target_password = args.password
        print(f"Target password set: '{target_password}'")
    elif args.interactive:
        target_password = getpass("Enter the password to crack: ")
        print("Target password set (hidden input)")
    elif args.hash:
        target_password = args.hash
        hash_mode = True
        print(f"Target hash set: '{target_password}'")
        print(f"Using hash algorithm: {args.algorithm}")
    
    # Initialize the brute forcer
    brute_forcer = BruteForceDemo()
    
    # Determine attack type
    using_wordlist = args.wordlist is not None
    
    if not using_wordlist:
        # Set charset based on arguments, or default if none provided
        use_lowercase = args.lowercase
        use_uppercase = args.uppercase
        use_digits = args.digits
        use_symbols = args.symbols
        
        # If no charset options selected, default to lowercase
        if not (use_lowercase or use_uppercase or use_digits or use_symbols):
            use_lowercase = True
        
        brute_forcer.set_charset(use_lowercase, use_uppercase, use_digits, use_symbols)
    
    try:
        # Start the attack
        if using_wordlist:
            print(f"Selected attack method: Dictionary attack")
            brute_forcer.dictionary_attack(target_password, args.wordlist, hash_mode, args.algorithm)
        else:
            print(f"Selected attack method: Brute force")
            brute_forcer.brute_force(target_password, args.max_length, hash_mode, args.algorithm)
    except KeyboardInterrupt:
        # Allow graceful exit with Ctrl+C
        elapsed = time.time() - brute_forcer.start_time
        print("\n\n[STOPPED] Attack interrupted by user")
        print(f"Attempts: {brute_forcer.attempts}")
        print(f"Time elapsed: {elapsed:.2f} seconds")
        rate = brute_forcer.attempts/elapsed if elapsed > 0 else 0
        print(f"Attempt rate: {rate:.2f} passwords/second")

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" BRUTE FORCE PASSWORD CRACKER - EDUCATIONAL DEMONSTRATION ")
    print("="*60)
    print("WARNING: This tool is for educational purposes only.\n")
    
    main()