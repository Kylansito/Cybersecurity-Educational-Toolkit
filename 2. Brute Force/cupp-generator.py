#!/usr/bin/env python3
"""
CUPP - Common User Passwords Profiler
A simple Python script to generate potential passwords based on personal information.
For educational purposes and security auditing only.
"""

import argparse
import itertools
import os
import datetime
import sys

class Cupp:
    def __init__(self):
        self.passwords = set()
        self.info = {}
        self.leet_map = {
            'a': ['4', '@'],
            'b': ['8'],
            'e': ['3'],
            'i': ['1', '!'],
            'l': ['1'],
            'o': ['0'],
            's': ['5', '$'],
            't': ['7', '+'],
        }
        self.special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '.']
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        
    def gather_info(self):
        """Gather personal information from user input"""
        print("\n[+] Please enter the information about the target or hit enter to skip.\n")
        
        self.info['first_name'] = input("[+] First name: ").lower()
        self.info['last_name'] = input("[+] Last name: ").lower()
        self.info['nickname'] = input("[+] Nickname: ").lower()
        
        while True:
            birth_date = input("[+] Birthdate (DDMMYYYY): ")
            if not birth_date:
                # Skip if empty
                self.info['birthdate'] = None
                break
            
            if len(birth_date) == 8 and birth_date.isdigit():
                day = birth_date[:2]
                month = birth_date[2:4]
                year = birth_date[4:]
                
                try:
                    # Validate date
                    datetime.datetime(int(year), int(month), int(day))
                    self.info['birthdate'] = {
                        'day': day,
                        'month': month,
                        'year': year,
                        'short_year': year[2:]
                    }
                    break
                except ValueError:
                    print("[-] Invalid date format. Please use DDMMYYYY.")
            else:
                print("[-] Invalid date format. Please use DDMMYYYY.")
        
        partner_info = input("[+] Include partner information? (y/n): ").lower() == 'y'
        if partner_info:
            self.info['partner_name'] = input("[+] Partner's name: ").lower()
            self.info['partner_nickname'] = input("[+] Partner's nickname: ").lower()
            
            while True:
                partner_birth = input("[+] Partner's birthdate (DDMMYYYY or enter to skip): ")
                if not partner_birth:
                    break
                    
                if len(partner_birth) == 8 and partner_birth.isdigit():
                    day = partner_birth[:2]
                    month = partner_birth[2:4]
                    year = partner_birth[4:]
                    
                    try:
                        # Validate date
                        datetime.datetime(int(year), int(month), int(day))
                        self.info['partner_birthdate'] = {
                            'day': day,
                            'month': month,
                            'year': year,
                            'short_year': year[2:]
                        }
                        break
                    except ValueError:
                        print("[-] Invalid date format. Please use DDMMYYYY.")
                else:
                    print("[-] Invalid date format. Please use DDMMYYYY.")
        
        child_info = input("[+] Include child's information? (y/n): ").lower() == 'y'
        if child_info:
            self.info['child_name'] = input("[+] Child's name: ").lower()
            self.info['child_nickname'] = input("[+] Child's nickname: ").lower()
            
            while True:
                child_birth = input("[+] Child's birthdate (DDMMYYYY or enter to skip): ")
                if not child_birth:
                    break
                    
                if len(child_birth) == 8 and child_birth.isdigit():
                    day = child_birth[:2]
                    month = child_birth[2:4]
                    year = child_birth[4:]
                    
                    try:
                        # Validate date
                        datetime.datetime(int(year), int(month), int(day))
                        self.info['child_birthdate'] = {
                            'day': day,
                            'month': month,
                            'year': year,
                            'short_year': year[2:]
                        }
                        break
                    except ValueError:
                        print("[-] Invalid date format. Please use DDMMYYYY.")
                else:
                    print("[-] Invalid date format. Please use DDMMYYYY.")
        
        self.info['pet'] = input("[+] Pet's name: ").lower()
        self.info['company'] = input("[+] Company name: ").lower()
        
        # Additional keywords
        print("\n[+] Enter additional keywords related to the target")
        print("[+] Examples: favorite athlete, favorite team, hobby, etc.")
        print("[+] Enter a blank line to finish.\n")
        
        keywords = []
        while True:
            keyword = input("[+] Keyword: ").lower()
            if not keyword:
                break
            keywords.append(keyword)
        
        self.info['keywords'] = keywords
        
        min_length = input("\n[+] Minimum password length (default: 4): ")
        if min_length.isdigit():
            self.min_length = int(min_length)
        else:
            self.min_length = 4
            
        max_length = input("[+] Maximum password length (default: 16): ")
        if max_length.isdigit():
            self.max_length = int(max_length)
        else:
            self.max_length = 16
            
        output_file = input("[+] Output file name (default: passwords.txt): ")
        self.output_file = output_file if output_file else "passwords.txt"
            
    def _add_password(self, password):
        """Add password to set if it meets length requirements"""
        if self.min_length <= len(password) <= self.max_length:
            self.passwords.add(password)
    
    def _generate_leet_variations(self, word):
        """Generate leetspeak variations of a word"""
        if not word:
            return []
            
        results = [word]
        
        # Generate all possible leet speak combinations
        for char, replacements in self.leet_map.items():
            if char in word:
                new_results = []
                for result in results:
                    new_results.append(result)
                    for replacement in replacements:
                        new_results.append(result.replace(char, replacement))
                results = new_results
                
        return results
    
    def _capitalize_variations(self, word):
        """Generate variations with different capitalizations"""
        if not word:
            return []
            
        results = [word, word.capitalize(), word.upper()]
        return results
    
    def generate_basic_passwords(self):
        """Generate basic password combinations"""
        print("\n[+] Generating basic passwords...")
        
        # Basic name combinations
        name_parts = [
            self.info.get('first_name', ''),
            self.info.get('last_name', ''),
            self.info.get('nickname', '')
        ]
        
        # Filter out empty strings
        name_parts = [part for part in name_parts if part]
        
        # Generate single parts and their variations
        for part in name_parts:
            cap_variants = self._capitalize_variations(part)
            for variant in cap_variants:
                self._add_password(variant)
                
            leet_variants = self._generate_leet_variations(part)
            for variant in leet_variants:
                self._add_password(variant)
                
        # Combinations of name parts
        for i in range(2, len(name_parts) + 1):
            for combo in itertools.permutations(name_parts, i):
                password = ''.join(combo)
                self._add_password(password)
                self._add_password(password.capitalize())
        
        # Name + numbers (years, common patterns)
        common_numbers = ['123', '1234', '12345', 'abc123']
        years = list(range(1950, datetime.datetime.now().year + 1))
        
        for part in name_parts:
            # Common number patterns
            for num in common_numbers:
                self._add_password(f"{part}{num}")
                self._add_password(f"{part.capitalize()}{num}")
                
            # Years
            for year in years:
                self._add_password(f"{part}{year}")
                self._add_password(f"{part.capitalize()}{year}")
                
        # Add birth date combinations if available
        if 'birthdate' in self.info and self.info['birthdate']:
            bd = self.info['birthdate']
            date_parts = [
                bd['day'],
                bd['month'],
                bd['year'],
                bd['short_year']
            ]
            
            # Add common date formats
            self._add_password(f"{bd['day']}{bd['month']}{bd['year']}")
            self._add_password(f"{bd['day']}{bd['month']}{bd['short_year']}")
            self._add_password(f"{bd['month']}{bd['day']}{bd['year']}")
            self._add_password(f"{bd['month']}{bd['day']}{bd['short_year']}")
            
            # Names with birth dates
            for part in name_parts:
                for date_part in date_parts:
                    self._add_password(f"{part}{date_part}")
                    self._add_password(f"{date_part}{part}")
                    self._add_password(f"{part.capitalize()}{date_part}")
                    
    def generate_complex_passwords(self):
        """Generate more complex password combinations"""
        print("[+] Generating complex passwords...")
        
        # Get all name-related strings
        all_names = []
        for key in ['first_name', 'last_name', 'nickname', 'partner_name', 
                  'partner_nickname', 'child_name', 'child_nickname', 'pet', 'company']:
            if key in self.info and self.info[key]:
                all_names.append(self.info[key])
                
        # Add keywords
        if 'keywords' in self.info:
            all_names.extend(self.info['keywords'])
            
        # Filter out empty strings
        all_names = [name for name in all_names if name]
        
        # Generate with special characters
        for name in all_names:
            cap_variants = self._capitalize_variations(name)
            
            for variant in cap_variants:
                # Add special chars at end
                for char in self.special_chars:
                    self._add_password(f"{variant}{char}")
                    
                    # Add numbers after special char
                    for num in range(10):
                        self._add_password(f"{variant}{char}{num}")
                        self._add_password(f"{variant}{num}{char}")
                        
            # Add combinations with birth years if available
            if 'birthdate' in self.info and self.info['birthdate']:
                year = self.info['birthdate']['year']
                short_year = self.info['birthdate']['short_year']
                
                for variant in cap_variants:
                    for char in self.special_chars:
                        self._add_password(f"{variant}{year}{char}")
                        self._add_password(f"{variant}{short_year}{char}")
                        self._add_password(f"{variant}{char}{year}")
                        self._add_password(f"{variant}{char}{short_year}")
        
        # Generate combinations of names and keywords
        if len(all_names) > 1:
            for i in range(len(all_names)):
                for j in range(len(all_names)):
                    if i != j:
                        combo = f"{all_names[i]}{all_names[j]}"
                        self._add_password(combo)
                        self._add_password(combo.capitalize())
                        
                        # Add numbers between
                        for num in range(10):
                            self._add_password(f"{all_names[i]}{num}{all_names[j]}")
                            
                        # Add special chars between
                        for char in self.special_chars:
                            self._add_password(f"{all_names[i]}{char}{all_names[j]}")
    
    def save_passwords(self):
        """Save generated passwords to file"""
        print(f"\n[+] Saving passwords to {self.output_file}...")
        
        try:
            with open(self.output_file, 'w') as f:
                for password in sorted(self.passwords):
                    f.write(f"{password}\n")
                    
            print(f"[+] {len(self.passwords)} passwords saved successfully.")
        except Exception as e:
            print(f"[-] Error saving passwords: {str(e)}")
    
    def run_interactive(self):
        """Run the password generator in interactive mode"""
        print("\n*****************************************")
        print("*   CUPP - Common User Passwords Profiler   *")
        print("*****************************************\n")
        
        self.gather_info()
        self.generate_basic_passwords()
        self.generate_complex_passwords()
        self.save_passwords()
        
    def run_from_file(self, config_file):
        """Run the password generator using a config file"""
        print(f"\n[+] Loading configuration from {config_file}...")
        
        try:
            # Implementation for loading from config file
            pass
        except Exception as e:
            print(f"[-] Error loading configuration: {str(e)}")
            return False
            
        self.generate_basic_passwords()
        self.generate_complex_passwords()
        self.save_passwords()
        return True

def main():
    parser = argparse.ArgumentParser(description='CUPP - Common User Passwords Profiler')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('-f', '--file', help='Use configuration file')
    
    args = parser.parse_args()
    
    cupp = Cupp()
    
    if args.interactive:
        cupp.run_interactive()
    elif args.file:
        cupp.run_from_file(args.file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()