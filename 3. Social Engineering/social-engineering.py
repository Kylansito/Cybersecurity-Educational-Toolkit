#!/usr/bin/env python3
###############################################################
# CATALAN-FOCUSED OSINT SOCIAL ENGINEERING TOOL
# WARNING: For educational purposes only. Use responsibly and ethically.
###############################################################

import os
import sys
import json
import time
import random
import requests
import re
import argparse
from datetime import datetime
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)

class CatalanOSINTCollector:
    """Class to perform OSINT gathering specific to Catalan targets"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # Common Catalan domains
        self.catalan_domains = [
            'gencat.cat', 'barcelona.cat', 'girona.cat', 'tarragona.cat', 'lleida.cat',
            'upc.edu', 'uab.cat', 'ub.edu', 'upf.edu', 'udg.edu', 'urv.cat'
        ]
        
        # Catalan newspapers and media
        self.catalan_media = [
            'lavanguardia.com', 'ara.cat', 'elperiodico.cat', 'elpuntavui.cat',
            'naciodigital.cat', 'vilaweb.cat', 'ccma.cat', 'rac1.cat', 'beteve.cat'
        ]
        
        # Common Catalan names
        self.common_catalan_names = [
            'Jordi', 'Marc', 'Josep', 'Joan', 'Pau', 'Oriol', 'Arnau', 'Roger', 'Albert', 'Xavier',
            'Montserrat', 'Núria', 'Anna', 'Maria', 'Laia', 'Marta', 'Laura', 'Carla', 'Mireia', 'Júlia'
        ]
        
        # Common Catalan last names
        self.common_catalan_surnames = [
            'Garcia', 'Martínez', 'López', 'Serra', 'Puig', 'Vila', 'Ferrer', 'Pujol', 'Vidal', 'Roca',
            'Soler', 'Roig', 'Costa', 'Mas', 'Casals', 'Rovira', 'Sala', 'Bosch', 'Torres', 'Català'
        ]
    
    def check_catalan_website(self, domain):
        """Check if website exists and has Catalan content"""
        
        urls = [f"https://www.{domain}", f"http://www.{domain}", f"https://{domain}", f"http://{domain}"]
        
        for url in urls:
            try:
                print(f"{Fore.BLUE}[*] Checking website: {url}{Style.RESET_ALL}")
                response = requests.get(url, headers=self.headers, timeout=5)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Check if the website has Catalan language elements
                    lang_tag = soup.html.get('lang', '').lower()
                    is_catalan = lang_tag in ['ca', 'ca-es']
                    
                    # Look for common Catalan words in content
                    text = soup.get_text().lower()
                    catalan_indicators = ['generalitat', 'catalunya', 'barcelona', 'girona', 
                                         'lleida', 'tarragona', 'ajuntament']
                    
                    catalan_words_found = [word for word in catalan_indicators if word in text]
                    
                    if is_catalan or catalan_words_found:
                        print(f"{Fore.GREEN}[+] Found Catalan website: {url}{Style.RESET_ALL}")
                        if catalan_words_found:
                            print(f"{Fore.GREEN}[+] Catalan indicators found: {', '.join(catalan_words_found)}{Style.RESET_ALL}")
                        
                        # Extract contact information
                        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
                        unique_emails = list(set(emails))
                        
                        phones = re.findall(r'(?:\+34|0034|34)?[\s-]?(?:6\d{2}|7[1-9]\d{1})[\s-]?\d{2}[\s-]?\d{2}[\s-]?\d{2}', response.text)
                        unique_phones = list(set(phones))
                        
                        if unique_emails:
                            print(f"{Fore.GREEN}[+] Emails found on website: {', '.join(unique_emails[:5])}{Style.RESET_ALL}")
                            if len(unique_emails) > 5:
                                print(f"{Fore.GREEN}   And {len(unique_emails)-5} more...{Style.RESET_ALL}")
                        
                        if unique_phones:
                            print(f"{Fore.GREEN}[+] Phone numbers found on website: {', '.join(unique_phones[:3])}{Style.RESET_ALL}")
                            if len(unique_phones) > 3:
                                print(f"{Fore.GREEN}   And {len(unique_phones)-3} more...{Style.RESET_ALL}")
                        
                        return {
                            'url': url,
                            'is_catalan': True,
                            'emails': unique_emails,
                            'phones': unique_phones,
                            'catalan_indicators': catalan_words_found
                        }
                        
            except Exception as e:
                print(f"{Fore.RED}[!] Error checking {url}: {str(e)}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}[!] No Catalan website found for {domain}{Style.RESET_ALL}")
        return None
    
    def check_linkedin_profile(self, name):
        """Check for LinkedIn profile based on name (educational only)"""
        # For educational purposes, we'll simulate the LinkedIn check
        # In a real implementation, you would use LinkedIn's API or web scraping
        
        print(f"{Fore.BLUE}[*] Searching for LinkedIn profiles for: {name}{Style.RESET_ALL}")
        
        # Simulate search delay
        time.sleep(1.5)
        
        # Generate a formatted name version (for URL construction)
        formatted_name = name.lower().replace(' ', '-')
        
        linkedin_url = f"https://www.linkedin.com/in/{formatted_name}"
        print(f"{Fore.GREEN}[+] Potential LinkedIn URL: {linkedin_url}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}[!] Note: Actual LinkedIn scraping requires authentication and may violate terms of service.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] For real OSINT, check LinkedIn manually or use commercial tools with proper authorization.{Style.RESET_ALL}")
        
        return {
            'name': name,
            'potential_linkedin_url': linkedin_url
        }
    
    def search_catalan_media(self, search_term):
        """Search for mentions in Catalan media"""
        print(f"{Fore.BLUE}[*] Searching Catalan media for: {search_term}{Style.RESET_ALL}")
        
        results = []
        
        # For each media site, construct a Google search URL
        for media in self.catalan_media[:3]:  # Limit to first 3 for demo
            search_url = f"https://www.google.com/search?q=site:{media}+{search_term.replace(' ', '+')}"
            print(f"{Fore.BLUE}[*] Searching: {media}{Style.RESET_ALL}")
            
            try:
                response = requests.get(search_url, headers=self.headers, timeout=5)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract search results (simplified)
                search_results = soup.find_all('div', class_='tF2Cxc')
                
                if search_results:
                    print(f"{Fore.GREEN}[+] Found {len(search_results)} mentions in {media}{Style.RESET_ALL}")
                    results.append({
                        'media': media,
                        'results_count': len(search_results)
                    })
                    
                time.sleep(2)  # Delay to avoid triggering Google's anti-scraping measures
                
            except Exception as e:
                print(f"{Fore.RED}[!] Error searching {media}: {str(e)}{Style.RESET_ALL}")
        
        return results
    
    def get_catalan_holidays(self):
        """Get upcoming Catalan holidays for better timing of social engineering"""
        catalan_holidays = [
            {"date": "2025-01-01", "name": "Any Nou", "description": "New Year's Day"},
            {"date": "2025-01-06", "name": "Reis", "description": "Epiphany"},
            {"date": "2025-04-18", "name": "Divendres Sant", "description": "Good Friday"},
            {"date": "2025-04-21", "name": "Dilluns de Pasqua", "description": "Easter Monday"},
            {"date": "2025-05-01", "name": "Dia del Treball", "description": "Labor Day"},
            {"date": "2025-06-24", "name": "Sant Joan", "description": "St. John's Day"},
            {"date": "2025-08-15", "name": "L'Assumpció", "description": "Assumption Day"},
            {"date": "2025-09-11", "name": "Diada Nacional", "description": "National Day of Catalonia"},
            {"date": "2025-09-24", "name": "La Mercè", "description": "Barcelona's local holiday"},
            {"date": "2025-10-12", "name": "Dia de la Hispanitat", "description": "Hispanic Day"},
            {"date": "2025-11-01", "name": "Tots Sants", "description": "All Saints' Day"},
            {"date": "2025-12-06", "name": "Dia de la Constitució", "description": "Constitution Day"},
            {"date": "2025-12-08", "name": "La Immaculada", "description": "Immaculate Conception"},
            {"date": "2025-12-25", "name": "Nadal", "description": "Christmas Day"},
            {"date": "2025-12-26", "name": "Sant Esteve", "description": "St. Stephen's Day"}
        ]
        
        today = datetime.now()
        upcoming_holidays = []
        
        for holiday in catalan_holidays:
            holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d')
            if holiday_date > today:
                days_until = (holiday_date - today).days
                if days_until <= 30:  # Only include holidays in the next 30 days
                    upcoming_holidays.append({
                        'name': holiday['name'],
                        'date': holiday['date'],
                        'days_until': days_until,
                        'description': holiday['description']
                    })
        
        return upcoming_holidays

class CatalanPhishingGenerator:
    """Class to generate targeted phishing attempts for Catalan targets"""
    
    def __init__(self):
        # Template subjects and bodies in both Catalan and Spanish
        self.templates = {
            "password_reset": {
                "subject": {
                    "ca": "Urgent: Cal restablir la contrasenya del seu compte [COMPANY]",
                    "es": "Urgente: Necesita restablecer la contraseña de su cuenta [COMPANY]"
                },
                "body": {
                    "ca": """
Benvolgut/da [NAME],

El nostre sistema de seguretat ha detectat una activitat de connexió inusual al seu compte [COMPANY]. Per protegir les seves dades, si us plau, restableixi la seva contrasenya immediatament fent clic a l'enllaç següent:

[LINK]

Si no ha intentat iniciar sessió, si us plau, restableixi la seva contrasenya immediatament i contacti amb el departament informàtic.

Gràcies,
Equip de Seguretat de [COMPANY]
                    """,
                    "es": """
Estimado/a [NAME],

Nuestro sistema de seguridad ha detectado una actividad de inicio de sesión inusual en su cuenta [COMPANY]. Para proteger sus datos, por favor, restablezca su contraseña inmediatamente haciendo clic en el siguiente enlace:

[LINK]

Si no ha intentado iniciar sesión, por favor, restablezca su contraseña inmediatamente y contacte con el departamento de informática.

Gracias,
Equipo de Seguridad de [COMPANY]
                    """
                }
            },
            "invoice": {
                "subject": {
                    "ca": "Factura #[RANDOM_NUM] Pagament pendent",
                    "es": "Factura #[RANDOM_NUM] Pago pendiente"
                },
                "body": {
                    "ca": """
Benvolgut/da [NAME],

Aquest és un recordatori que la factura #[RANDOM_NUM] per [AMOUNT] està pendent de pagament.

Si us plau, revisi la factura adjunta i processi el pagament el més aviat possible fent clic aquí: [LINK]

Si té alguna pregunta, contacti amb el nostre departament de comptabilitat.

Atentament,
[SENDER_NAME]
Departament de Comptabilitat
[COMPANY]
                    """,
                    "es": """
Estimado/a [NAME],

Este es un recordatorio de que la factura #[RANDOM_NUM] por [AMOUNT] está pendiente de pago.

Por favor, revise la factura adjunta y procese el pago lo antes posible haciendo clic aquí: [LINK]

Si tiene alguna pregunta, contacte con nuestro departamento de contabilidad.

Atentamente,
[SENDER_NAME]
Departamento de Contabilidad
[COMPANY]
                    """
                }
            },
            "shared_document": {
                "subject": {
                    "ca": "Document important compartit amb vostè",
                    "es": "Documento importante compartido con usted"
                },
                "body": {
                    "ca": """
Hola [NAME],

[SENDER_NAME] ha compartit un document important amb vostè que requereix la seva revisió.

Document: [DOCUMENT_NAME]
Missatge: "[MESSAGE]"

Pot accedir al document aquí: [LINK]

Aquest enllaç caducarà en 24 hores.

Salutacions,
Sistema de compartició de documents de [COMPANY]
                    """,
                    "es": """
Hola [NAME],

[SENDER_NAME] ha compartido un documento importante con usted que requiere su revisión.

Documento: [DOCUMENT_NAME]
Mensaje: "[MESSAGE]"

Puede acceder al documento aquí: [LINK]

Este enlace caducará en 24 horas.

Saludos,
Sistema de compartición de documentos de [COMPANY]
                    """
                }
            },
            "generalitat_update": {
                "subject": {
                    "ca": "Actualització important de la Generalitat de Catalunya",
                    "es": "Actualización importante de la Generalitat de Cataluña"
                },
                "body": {
                    "ca": """
Benvolgut/da [NAME],

La Generalitat de Catalunya ha actualitzat la normativa que afecta el seu sector. Com a [POSITION] de [COMPANY], és important que revisi els canvis i actualitzi la seva documentació.

Per accedir als nous formularis i guies, faci clic aquí: [LINK]

Data límit per a la implementació: [DEADLINE]

Si necessita assistència, pot contactar amb el nostre servei d'ajuda.

Atentament,
Departament [DEPARTMENT]
Generalitat de Catalunya
                    """,
                    "es": """
Estimado/a [NAME],

La Generalitat de Cataluña ha actualizado la normativa que afecta a su sector. Como [POSITION] de [COMPANY], es importante que revise los cambios y actualice su documentación.

Para acceder a los nuevos formularios y guías, haga clic aquí: [LINK]

Fecha límite para la implementación: [DEADLINE]

Si necesita asistencia, puede contactar con nuestro servicio de ayuda.

Atentamente,
Departamento [DEPARTMENT]
Generalitat de Cataluña
                    """
                }
            },
            "bank_notification": {
                "subject": {
                    "ca": "Notificació important sobre el seu compte - [BANK_NAME]",
                    "es": "Notificación importante sobre su cuenta - [BANK_NAME]"
                },
                "body": {
                    "ca": """
Benvolgut/da client/a [NAME],

Ens posem en contacte des de [BANK_NAME] per informar-lo d'un canvi important en la normativa de seguretat. Per seguir accedint al seu compte, ha de verificar la seva identitat seguint aquests passos:

1. Accedeixi al seu compte a través d'aquest enllaç segur: [LINK]
2. Actualitzi les seves dades de contacte
3. Confirmi la seva identitat amb el codi que rebrà al seu telèfon

Aquesta actualització és obligatòria abans del [DEADLINE].

Atentament,
Equip de Seguretat
[BANK_NAME]
                    """,
                    "es": """
Estimado/a cliente [NAME],

Nos ponemos en contacto desde [BANK_NAME] para informarle de un cambio importante en la normativa de seguridad. Para seguir accediendo a su cuenta, debe verificar su identidad siguiendo estos pasos:

1. Acceda a su cuenta a través de este enlace seguro: [LINK]
2. Actualice sus datos de contacto
3. Confirme su identidad con el código que recibirá en su teléfono

Esta actualización es obligatoria antes del [DEADLINE].

Atentamente,
Equipo de Seguridad
[BANK_NAME]
                    """
                }
            }
        }
        
        # Catalan-specific banks for templates
        self.catalan_banks = [
            'CaixaBank', 'Banc Sabadell', 'BBVA Catalunya', 'Banco Santander', 
            'Kutxabank Catalunya', 'Catalunya Caixa'
        ]
        
        # Generalitat departments
        self.departments = [
            'Salut', 'Educació', 'Economia i Hisenda', 'Cultura', 'Empresa i Treball',
            'Acció Climàtica', 'Interior', 'Justícia', 'Drets Socials', 'Recerca i Universitats'
        ]
    
    def generate_phishing_email(self, target, template_name, language="ca"):
        """Generate a targeted phishing email based on collected information"""
        if template_name not in self.templates:
            print(f"{Fore.RED}[!] Template not found{Style.RESET_ALL}")
            return None
        
        if language not in ["ca", "es"]:
            print(f"{Fore.RED}[!] Unsupported language. Using Catalan (ca) instead.{Style.RESET_ALL}")
            language = "ca"
        
        template = self.templates[template_name]
        
        # Get subject and body in selected language
        subject = template["subject"][language]
        body = template["body"][language]
        
        # Replace placeholders
        replacements = {
            "[NAME]": target.get("name", ""),
            "[COMPANY]": target.get("company", ""),
            "[POSITION]": target.get("position", ""),
            "[LINK]": f"https://securit-y-update.{target.get('company', '').lower().replace(' ', '')}.{random.choice(['online', 'site', 'app'])}/login",
            "[RANDOM_NUM]": str(random.randint(10000, 99999)),
            "[AMOUNT]": f"{random.randint(100, 9999)},{random.randint(0, 99):02d}€",
            "[SENDER_NAME]": random.choice([
                "Albert Ferrer", "Montserrat Vila", "Jordi Puig", "Núria Casals", "Roger Martí", "Laia Soler"
            ]),
            "[DOCUMENT_NAME]": random.choice([
                f"{target.get('company', '')} - Informe Trimestral.pdf",
                "Pla Estratègic 2025.docx",
                "Acta Reunió Equip.pdf",
                f"Actualització Projecte - {time.strftime('%B %Y')}.xlsx",
                "Confidencial - Revisió Pressupost.pdf",
                f"Important - Actualització Normativa {target.get('company', '')}.pdf"
            ]),
            "[MESSAGE]": random.choice([
                "Si us plau, reviseu-ho abans d'avui",
                "Necessito la vostra opinió sobre això",
                "Actualització important - reviseu-ho urgentment",
                "Per a la vostra revisió abans de la reunió de demà",
                "Urgent - requereix la vostra aprovació",
                "Informació confidencial - només per als vostres ulls"
            ]) if language == "ca" else random.choice([
                "Por favor, revíselo antes de hoy",
                "Necesito su opinión sobre esto",
                "Actualización importante - revíselo urgentemente",
                "Para su revisión antes de la reunión de mañana",
                "Urgente - requiere su aprobación",
                "Información confidencial - solo para sus ojos"
            ]),
            "[BANK_NAME]": random.choice(self.catalan_banks),
            "[DEPARTMENT]": random.choice(self.departments),
            "[DEADLINE]": (datetime.now().strftime("%d/%m/%Y"))
        }
        
        for placeholder, value in replacements.items():
            subject = subject.replace(placeholder, value)
            body = body.replace(placeholder, value)
        
        # Add personalization based on target information
        if language == "ca":
            if target.get("interests") and template_name == "shared_document":
                body += f"\n\nP.D.: He vist que esteu interessat en {target.get('interests')}. Podríem parlar-ne algun dia!"
        else:
            if target.get("interests") and template_name == "shared_document":
                body += f"\n\nP.D.: He visto que está interesado en {target.get('interests')}. ¡Podríamos hablar de ello algún día!"
        
        return {
            "to": target.get("email", ""),
            "subject": subject,
            "body": body,
            "language": language
        }
    
    def display_email(self, email):
        """Display the generated phishing email"""
        print("\n" + "=" * 60)
        print(f"{Fore.RED}SIMULATED PHISHING EMAIL (EDUCATIONAL DEMO ONLY){Style.RESET_ALL}")
        print("=" * 60)
        print(f"{Fore.YELLOW}To:{Style.RESET_ALL} {email['to']}")
        print(f"{Fore.YELLOW}Subject:{Style.RESET_ALL} {email['subject']}")
        print(f"{Fore.YELLOW}Language:{Style.RESET_ALL} {email['language']}")
        print("-" * 60)
        print(email['body'])
        print("=" * 60)
        
        # Highlight the attack vectors
        print(f"\n{Fore.GREEN}ATTACK VECTORS USED:{Style.RESET_ALL}")
        print(f"1. {Fore.YELLOW}Social Engineering:{Style.RESET_ALL} Using authority and urgency to prompt action")
        print(f"2. {Fore.YELLOW}Regionalization:{Style.RESET_ALL} Using Catalan language and local context")
        print(f"3. {Fore.YELLOW}Personalization:{Style.RESET_ALL} Using target's name, company, and position")
        print(f"4. {Fore.YELLOW}Disguised URL:{Style.RESET_ALL} Using a domain that looks legitimate")
        print(f"5. {Fore.YELLOW}Cultural Context:{Style.RESET_ALL} Leveraging local institutions like Generalitat")
        
        
        print(f"\n{Fore.RED}REMINDER: This is for educational purposes only. Never use these techniques for actual phishing.{Style.RESET_ALL}")

def main():
    """Main function to run the OSINT and phishing tool"""
    parser = argparse.ArgumentParser(description='Catalan-Focused OSINT Social Engineering Tool')
    parser.add_argument('-t', '--target', help='Target name')
    parser.add_argument('-e', '--email', help='Target email')
    parser.add_argument('-c', '--company', help='Target company or organization')
    parser.add_argument('-p', '--position', help='Target job position')
    parser.add_argument('-d', '--domain', help='Company domain to scan')
    parser.add_argument('-l', '--language', choices=['ca', 'es'], default='ca', help='Language for phishing email (ca=Catalan, es=Spanish)')
    
    args = parser.parse_args()
    
    print(f"{Fore.GREEN}=" * 70)
    print(f"CATALAN-FOCUSED OSINT SOCIAL ENGINEERING TOOL")
    print(f"=" * 70)
    print(f"{Fore.RED}WARNING: This tool is for educational purposes only.{Style.RESET_ALL}")
    print(f"{Fore.RED}Using these tools against individuals without permission is illegal.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}=" * 70 + Style.RESET_ALL)
    
    # Initialize collectors
    osint_collector = CatalanOSINTCollector()
    phishing_generator = CatalanPhishingGenerator()
    
    # Target information
    target = {}
    
    # If no command-line arguments, prompt user for input
    if not (args.target or args.email or args.company):
        print(f"{Fore.BLUE}[*] No target specified. Please enter information:{Style.RESET_ALL}")
        
        target["name"] = args.target or input("Target's name: ")
        target["email"] = args.email or input("Target's email: ")
        target["company"] = args.company or input("Target's company: ")
        target["position"] = args.position or input("Target's job position: ")
        domain = args.domain or input("Company domain (e.g., company.cat): ")
    else:
        target["name"] = args.target if args.target else input("Target's name: ")
        target["email"] = args.email if args.email else input("Target's email: ")
        target["company"] = args.company if args.company else input("Target's company: ")
        target["position"] = args.position if args.position else input("Target's job position: ")
        domain = args.domain if args.domain else input("Company domain (e.g., company.cat): ")
    
    # Gather OSINT information
    print(f"\n{Fore.BLUE}[*] Beginning OSINT gathering for {target['name']} at {target['company']}{Style.RESET_ALL}")
    
    # Check for website
    if domain:
        website_info = osint_collector.check_catalan_website(domain)
        if website_info:
            target["website"] = website_info["url"]
            if website_info.get("emails"):
                target["company_emails"] = website_info["emails"]
            if website_info.get("phones"):
                target["company_phones"] = website_info["phones"]
    
    # Check LinkedIn
    linkedin_info = osint_collector.check_linkedin_profile(target["name"])
    if linkedin_info:
        target["linkedin"] = linkedin_info["potential_linkedin_url"]
    
    # Search mentions in Catalan media
    media_mentions = osint_collector.search_catalan_media(f"{target['name']} {target['company']}")
    if media_mentions:
        target["media_mentions"] = media_mentions
    
    # Get Catalan holidays for timing
    upcoming_holidays = osint_collector.get_catalan_holidays()
    if upcoming_holidays:
        print(f"\n{Fore.GREEN}[+] Upcoming Catalan holidays (useful for timing attacks):{Style.RESET_ALL}")
        for holiday in upcoming_holidays:
            print(f"  - {holiday['name']} ({holiday['date']}): {holiday['days_until']} days away")
        
        # Add holiday to target info for potential use
        target["upcoming_holiday"] = upcoming_holidays[0] if upcoming_holidays else None
    
    # Generate random interests for demonstration (in a real tool, this would be from OSINT)
    catalan_interests = [
        "FC Barcelona", "cuina catalana", "vi del Penedès", "castellers", "sardanes", 
        "Pirineus", "Costa Brava", "cultura catalana", "senderisme", "literatura catalana"
    ]
    spanish_interests = [
        "fútbol", "gastronomía", "vinos", "senderismo", "literatura", 
        "montañas", "playa", "cultura", "viajes", "deportes"
    ]
    
    target["interests"] = random.choice(catalan_interests if args.language == "ca" else spanish_interests)
    
    # Display gathered information
    print(f"\n{Fore.GREEN}[+] OSINT Information Gathered:{Style.RESET_ALL}")
    for key, value in target.items():
        if key not in ["company_emails", "company_phones", "media_mentions", "upcoming_holiday"]:
            print(f"  - {key.capitalize()}: {value}")
    
    # Generate phishing email
    print(f"\n{Fore.BLUE}[*] Generating targeted phishing email...{Style.RESET_ALL}")
    
    # Let user choose a template
    print(f"\n{Fore.GREEN}[*] Available Phishing Templates:{Style.RESET_ALL}")
    print(f"1. Password Reset")
    print(f"2. Invoice Payment")
    print(f"3. Shared Document")
    print(f"4. Generalitat Update (Government)")
    print(f"5. Bank Notification")
    
    choice = input("\nSelect template (1-5): ")
    template_map = {
        "1": "password_reset", 
        "2": "invoice", 
        "3": "shared_document",
        "4": "generalitat_update",
        "5": "bank_notification"
    }
    
    if choice in template_map:
        template_name = template_map[choice]
        email = phishing_generator.generate_phishing_email(target, template_name, args.language)
        if email:
            phishing_generator.display_email(email)
            
            # Offer to customize the email further
            if input("\nWould you like to customize this email further? (y/n): ").lower() == 'y':
                print("\nWhat would you like to customize?")
                print("1. Add local Catalan event reference")
                print("2. Make it more urgent")
                print("3. Add an attachment reference")
                print("4. Add a personal detail from OSINT")
                
                custom_choice = input("\nSelect customization (1-4): ")
                
                if custom_choice == "1" and target.get("upcoming_holiday"):
                    holiday = target["upcoming_holiday"]
                    if args.language == "ca":
                        email["body"] += f"\n\nP.D.: Donat que s'apropa {holiday['name']} ({holiday['date']}), necessitem completar aquesta acció abans de la festivitat."
                    else:
                        email["body"] += f"\n\nP.D.: Dado que se acerca {holiday['name']} ({holiday['date']}), necesitamos completar esta acción antes de la festividad."
                    phishing_generator.display_email(email)
                
                elif custom_choice == "2":
                    if args.language == "ca":
                        email["body"] += "\n\nACTUALITZACIÓ URGENT: Aquest assumpte ara és extremadament urgent. Si us plau, respongui dins de les properes 2 hores per evitar la suspensió del compte."
                        email["subject"] = "URGENT: " + email["subject"]
                    else:
                        email["body"] += "\n\nACTUALIZACIÓN URGENTE: Este asunto ahora es extremadamente urgente. Por favor, responda dentro de las próximas 2 horas para evitar la suspensión de la cuenta."
                        email["subject"] = "URGENTE: " + email["subject"]
                    phishing_generator.display_email(email)
                
                elif custom_choice == "3":
                    attachment_name = input("Enter attachment name (e.g. 'Factura.pdf'): ")
                    if args.language == "ca":
                        email["body"] += f"\n\nConsulti el fitxer adjunt {attachment_name} per més detalls."
                    else:
                        email["body"] += f"\n\nConsulte el archivo adjunto {attachment_name} para más detalles."
                    print(f"\n{Fore.YELLOW}[*] In a real attack, this would include a malicious attachment: {attachment_name}{Style.RESET_ALL}")
                    phishing_generator.display_email(email)
                
                elif custom_choice == "4":
                    if args.language == "ca":
                        email["body"] += f"\n\nPer cert, he vist que vostè {random.choice(['és aficionat al', 'té interès en', 'segueix el'])} {target.get('interests')}. Això pot ser també d'interès per a vostè."
                    else:
                        email["body"] += f"\n\nPor cierto, he visto que usted {random.choice(['es aficionado al', 'tiene interés en', 'sigue el'])} {target.get('interests')}. Esto también puede ser de interés para usted."
                    phishing_generator.display_email(email)
    else:
        print(f"{Fore.RED}[!] Invalid choice{Style.RESET_ALL}")
    
    # Educational component - detection and prevention
    print(f"\n{Fore.GREEN}=" * 70)
    print(f"EDUCATIONAL NOTES FOR PRESENTATION")
    print(f"=" * 70 + f"{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}Catalan-Specific Social Engineering Factors:{Style.RESET_ALL}")
    print(" 1. Language choice (Catalan vs Spanish) can influence trust")
    print(" 2. Local institutions (Generalitat, Ajuntaments) lend credibility")
    print(" 3. Regional holidays and events provide timely pretexts")
    print(" 4. Local business and cultural references increase believability")
    print(" 5. Dual-language environment creates opportunity for mistakes/confusion")
    
    print(f"\n{Fore.YELLOW}Protective Measures to Teach:{Style.RESET_ALL}")
    print(" 1. Verify sender through alternate trusted channels")
    print(" 2. Be wary of language switching or unusual language choice")
    print(" 3. Check URLs carefully - government domains end in .gencat.cat, .barcelona.cat, etc.")
    print(" 4. Enable 2FA for all important accounts")
    print(" 5. Report suspicious messages to IT security teams")
    
    # Offer to run again or exit
    if input(f"\n{Fore.BLUE}Would you like to create another phishing simulation? (y/n): {Style.RESET_ALL}").lower() == 'y':
        main()
    else:
        print(f"\n{Fore.GREEN}[*] Exiting program. Thank you for using the educational tool.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()