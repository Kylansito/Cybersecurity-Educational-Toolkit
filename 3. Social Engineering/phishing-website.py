from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import qrcode
from datetime import datetime
import json

app = Flask(__name__)

# Directory for storing templates and static files
if not os.path.exists('templates'):
    os.makedirs('templates')
if not os.path.exists('static'):
    os.makedirs('static')

# Store captured data temporarily (for educational demo only)
captured_data = []

# Create HTML files
def setup_html_files():
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create the phishing page HTML
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CaixaBank - Iniciar sessió</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }
        
        body {
            background-color: #f5f5f5;
        }
        
        .warning-banner {
            background-color: #ff4c4c;
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 16px;
            font-weight: bold;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            background-color: #fff;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .logo {
            width: 180px;
        }
        
        .nav {
            display: flex;
        }
        
        .nav-item {
            margin-left: 20px;
            color: #666;
            text-decoration: none;
            font-size: 14px;
        }
        
        .main {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .login-box {
            flex: 1;
            min-width: 350px;
            background-color: #fff;
            padding: 25px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .info-box {
            flex: 1;
            min-width: 350px;
            background-color: #007AC2;
            color: white;
            padding: 25px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        h1 {
            font-size: 24px;
            margin-bottom: 20px;
            color: #333;
        }
        
        .info-box h1 {
            color: white;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-size: 14px;
            color: #555;
        }
        
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        
        button {
            background-color: #007AC2;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 12px 20px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
        }
        
        button:hover {
            background-color: #005a8e;
        }
        
        .forgot-link {
            display: block;
            text-align: center;
            margin-top: 15px;
            color: #007AC2;
            text-decoration: none;
            font-size: 14px;
        }
        
        .info-list {
            margin-top: 20px;
            padding-left: 20px;
        }
        
        .info-list li {
            margin-bottom: 10px;
            font-size: 14px;
        }
        
        .footer {
            margin-top: 40px;
            text-align: center;
            color: #777;
            font-size: 12px;
        }
        
        .footer a {
            color: #007AC2;
            text-decoration: none;
        }
        
        .security-badge {
            display: flex;
            align-items: center;
            margin-top: 15px;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 5px;
            border: 1px solid #eee;
        }
        
        .security-badge span {
            margin-left: 10px;
            font-size: 12px;
            color: #777;
        }
        
        .lock-icon {
            color: #007AC2;
            font-size: 18px;
        }
        
        @media (max-width: 768px) {
            .main {
                flex-direction: column;
            }
            
            .nav {
                display: none;
            }
        }
    </style>
</head>
<body>
    <div class="warning-banner">
        EINA EDUCATIVA - NO INTRODUÏU CREDENCIALS REALS - DEMOSTRACIÓ DE SEGURETAT
    </div>
    
    <div class="container">
        <div class="header">
            <img src="/static/logo.png" alt="CaixaBank" class="logo">
            <div class="nav">
                <a href="#" class="nav-item">Particulars</a>
                <a href="#" class="nav-item">Empreses</a>
                <a href="#" class="nav-item">Banca Privada</a>
                <a href="#" class="nav-item">Informació Corporativa</a>
            </div>
        </div>
        
        <div class="main">
            <div class="login-box">
                <h1>Accés a CaixaBankNow</h1>
                <form id="login-form" action="/login" method="post">
                    <div class="form-group">
                        <label for="username">Identificador (NIF/NIE/Passaport)</label>
                        <input type="text" id="username" name="username" placeholder="Introduïu el vostre identificador" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="password">Contrasenya d'accés</label>
                        <input type="password" id="password" name="password" placeholder="Introduïu la vostra contrasenya" required>
                    </div>
                    
                    <button type="submit">Iniciar sessió</button>
                    
                    <a href="#" class="forgot-link">He oblidat la meva contrasenya</a>
                    
                    <div class="security-badge">
                        <span class="lock-icon">🔒</span>
                        <span>Connexió segura. Les teves dades viatgen xifrades.</span>
                    </div>
                </form>
            </div>
            
            <div class="info-box">
                <h1>Mesures de seguretat importants</h1>
                <p>Recorda que CaixaBank mai et demanarà:</p>
                <ul class="info-list">
                    <li>Les teves claus completes de CaixaBankNow per telèfon, SMS o correu electrònic</li>
                    <li>Codis de confirmació d'operacions que no hagis sol·licitat</li>
                    <li>Informació personal sensible per realitzar gestions</li>
                </ul>
                <p style="margin-top: 20px;">Consulta les nostres recomanacions de seguretat per protegir els teus comptes i accedir als serveis de CaixaBank de manera segura.</p>
                </div>
            </div>
            
            <div class="footer">
                <p>© CaixaBank, S.A. Tots els drets reservats.</p>
                <p>Av. Diagonal, 621, 08028 Barcelona</p>
                <p><a href="#">Política de privacitat</a> | <a href="#">Avís legal</a> | <a href="#">Cookies</a></p>
                <p style="margin-top: 10px; color: #ff4c4c; font-weight: bold;">
                    AQUESTA ÉS UNA SIMULACIÓ DE CIBERATAC AMB FINALITATS EDUCATIVES
                </p>
            </div>
        </div>
    </body>
    </html>''')
    
    # Create the educational page HTML
    with open('templates/educational.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulació de Phishing - Pàgina Educativa</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }
        
        body {
            background-color: #f5f5f5;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: #fff;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        h1 {
            color: #d32f2f;
            margin-bottom: 10px;
            font-size: 28px;
        }
        
        .subtitle {
            color: #555;
            font-size: 18px;
        }
        
        .section {
            margin-bottom: 30px;
        }
        
        h2 {
            color: #333;
            margin-bottom: 15px;
            font-size: 22px;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
        
        p {
            color: #555;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        
        ul, ol {
            margin-left: 20px;
            margin-bottom: 15px;
        }
        
        li {
            margin-bottom: 10px;
            line-height: 1.5;
        }
        
        .alert-box {
            background-color: #ffebee;
            border-left: 4px solid #d32f2f;
            padding: 15px;
            margin-bottom: 20px;
        }
        
        .tip-box {
            background-color: #e8f5e9;
            border-left: 4px solid #43a047;
            padding: 15px;
            margin-bottom: 20px;
        }
        
        .comparison {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .comparison-col {
            flex: 1;
            min-width: 300px;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }
        
        .comparison-col h3 {
            margin-bottom: 10px;
            color: #333;
        }
        
        .comparison-col.fake {
            background-color: #ffebee;
        }
        
        .comparison-col.real {
            background-color: #e8f5e9;
        }
        
        .img-container {
            text-align: center;
            margin: 20px 0;
        }
        
        img {
            max-width: 100%;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #777;
            font-size: 14px;
        }
        
        .highlight {
            background-color: #fffde7;
            padding: 2px 5px;
            border-radius: 3px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background-color: #f5f5f5;
        }
        
        .button {
            display: inline-block;
            background-color: #4caf50;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 4px;
            font-weight: bold;
            margin-top: 10px;
        }
        
        .button:hover {
            background-color: #43a047;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Has participat en una simulació d'atac de phishing!</h1>
            <p class="subtitle">Aquesta és una activitat educativa per entendre com funcionen els atacs de phishing i com protegir-se.</p>
        </header>
        
        <div class="section">
            <div class="alert-box">
                <h3>Important: Simulació educativa</h3>
                <p>Aquesta ha estat una simulació controlada. Cap credencial introduïda ha estat emmagatzemada de forma permanent. Aquesta demostració forma part d'una activitat formativa de ciberseguretat.</p>
            </div>
        </div>
        
        <div class="section">
            <h2>Què acaba de passar?</h2>
            <p>Has participat en una simulació d'un atac de <strong>phishing</strong>, una tècnica d'enginyeria social que els ciberdelinqüents utilitzen per enganyar els usuaris i fer que revelin informació confidencial.</p>
            
            <p>El lloc web que acabes de visitar és una <strong>rèplica falsa</strong> dissenyada per semblar el lloc legítim de CaixaBank. Els atacants sovint creen còpies gairebé idèntiques de llocs web populars per enganyar els usuaris i robar les seves credencials.</p>
        </div>
        
        <div class="section">
            <h2>Com identificar un atac de phishing?</h2>
            
            <div class="comparison">
                <div class="comparison-col fake">
                    <h3>Lloc fals (com el que has vist)</h3>
                    <ul>
                        <li>URL incorrecta (no acaba en caixabank.es/com)</li>
                        <li>Manca el certificat de seguretat vàlid</li>
                        <li>Pot contenir petits errors d'ortografia o disseny</li>
                        <li>Pressió per actuar ràpidament</li>
                        <li>Enllaços que no apunten a pàgines oficials</li>
                    </ul>
                </div>
                
                <div class="comparison-col real">
                    <h3>Lloc legítim (el real)</h3>
                    <ul>
                        <li>URL correcta (caixabank.es o caixabank.com)</li>
                        <li>Connexió segura (cadenat verd i https://)</li>
                        <li>Disseny i ortografia perfectes</li>
                        <li>No utilitza tàctiques de pressió</li>
                        <li>Tots els enllaços apunten a dominis oficials</li>
                    </ul>
                </div>
            </div>
            
            <div class="tip-box">
                <h3>Consells de seguretat:</h3>
                <ol>
                    <li><strong>Verifica sempre la URL</strong> abans d'introduir les teves credencials. Assegura't que comença amb <span class="highlight">https://</span> i correspon exactament al domini oficial.</li>
                    <li><strong>No facis clic en enllaços</strong> rebuts per correu electrònic o missatges. És millor accedir directament a la pàgina web escrivint l'adreça al navegador.</li>
                    <li><strong>Activa l'autenticació de doble factor</strong> sempre que sigui possible.</li>
                    <li><strong>Mantingues actualitzat</strong> el navegador i el sistema operatiu.</li>
                    <li><strong>Desconfia</strong> dels missatges que generen urgència o por.</li>
                </ol>
            </div>
        </div>
        
        <div class="section">
            <h2>Elements d'enginyeria social utilitzats</h2>
            <table>
                <tr>
                    <th>Tècnica</th>
                    <th>Com es va utilitzar</th>
                    <th>Com protegir-se</th>
                </tr>
                <tr>
                    <td>Suplantació d'identitat visual</td>
                    <td>Còpia exacta del disseny de CaixaBank</td>
                    <td>Verificar sempre la URL</td>
                </tr>
                <tr>
                    <td>Creació de confiança</td>
                    <td>Ús d'elements de seguretat falsos</td>
                    <td>Comprovar els certificats de seguretat</td>
                </tr>
                <tr>
                    <td>Contextualització</td>
                    <td>Ús del català i elements regionals</td>
                    <td>Confirmar per canals alternatius</td>
                </tr>
                <tr>
                    <td>Aprofitament de l'autoritat</td>
                    <td>Impersonació d'una entitat bancària oficial</td>
                    <td>Contactar directament amb l'entitat</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>Estadístiques sobre phishing</h2>
            <ul>
                <li>El <strong>90%</strong> de les filtracions de dades comencen amb un atac de phishing</li>
                <li>Més del <strong>30%</strong> dels correus de phishing són oberts pels destinataris</li>
                <li>El <strong>12%</strong> dels usuaris fan clic en enllaços maliciosos o adjunts</li>
                <li>El cost mitjà d'un atac de phishing per a una empresa mitjana és de <strong>120.000€</strong></li>
                <li>Els sectors més atacats són: finances, salut, educació i administració pública</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>Com reportar un atac real?</h2>
            <p>Si creus que has estat víctima d'un atac de phishing real:</p>
            <ol>
                <li>Canvia immediatament les contrasenyes dels comptes afectats</li>
                <li>Contacta amb la teva entitat bancària o servei afectat</li>
                <li>Reporta l'incident a través de l'INCIBE (Institut Nacional de Ciberseguretat):
                    <br>Telèfon: <strong>017</strong>
                    <br>Web: <strong>incibe.es</strong>
                </li>
                <li>Si has patit un frau econòmic, presenta una denúncia a la policia</li>
            </ol>
        </div>
        
        <div class="footer">
            <p>Aquesta simulació ha estat creada amb finalitats educatives com a part d'una presentació de ciberseguretat.</p>
            <p>© 2025 - Tots els drets reservats</p>
            <a href="/" class="button">Tornar a l'inici</a>
        </div>
    </div>
</body>
</html>''')
    
    # Create admin page for viewing results
    with open('templates/admin.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Administració Demo Phishing</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }
        
        body {
            background-color: #f5f5f5;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: #fff;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #777;
            font-size: 16px;
        }
        
        .warning-banner {
            background-color: #ff4c4c;
            color: white;
            text-align: center;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            font-weight: bold;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        
        tr:hover {
            background-color: #f9f9f9;
        }
        
        .no-data {
            text-align: center;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 5px;
            color: #777;
        }
        
        .button {
            display: inline-block;
            background-color: #4caf50;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 4px;
            margin-top: 20px;
        }
        
        .button.red {
            background-color: #f44336;
        }
        
        .qr-section {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }
        
        .qr-container {
            margin-top: 20px;
            text-align: center;
        }
        
        .qr-image {
            max-width: 250px;
            border: 1px solid #ddd;
        }
        
        .footer {
            margin-top: 30px;
            text-align: center;
            color: #777;
            font-size: 14px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Administració de la Demo de Phishing</h1>
            <p class="subtitle">Aquesta pàgina és només per a l'instructor de la sessió de ciberseguretat</p>
        </header>
        
        <div class="warning-banner">
            AQUESTA INFORMACIÓ ÉS TEMPORAL I S'ELIMINARÀ EN ACABAR LA DEMOSTRACIÓ
        </div>
        
        <h2>Resultats de la Simulació</h2>
        
        {% if captured_data %}
        <table>
            <tr>
                <th>Identificador</th>
                <th>Contrasenya</th>
                <th>Data i Hora</th>
                <th>Adreça IP</th>
            </tr>
            {% for entry in captured_data %}
            <tr>
                <td>{{ entry.username }}</td>
                <td>{{ entry.password }}</td>
                <td>{{ entry.timestamp }}</td>
                <td>{{ entry.ip }}</td>
            </tr>
            {% endfor %}
        </table>
        <a href="/admin/clear" class="button red">Esborrar totes les dades</a>
        {% else %}
        <div class="no-data">
            <p>Encara no hi ha dades capturades en aquesta simulació.</p>
        </div>
        {% endif %}
        
        <div class="qr-section">
            <h2>Codi QR per compartir</h2>
            <p>Comparteix aquest codi QR amb els participants per accedir a la simulació:</p>
            <div class="qr-container">
                <img src="{{ url_for('static', filename='qr_code.png') }}" alt="QR Code" class="qr-image">
            </div>
            <p>URL de la demostració: <strong>{{ demo_url }}</strong></p>
        </div>
        
        <div class="footer">
            <p>Eina educativa de ciberseguretat - Només per a fins demostratius</p>
            <a href="/" class="button">Tornar a l'inici</a>
        </div>
    </div>
</body>
</html>''')

def generate_qr_code(url):
    """Generate QR code for the phishing demo URL"""
    img = qrcode.make(url)
    img.save('static/qr_code.png')
    return 'static/qr_code.png'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """Handle login attempts and capture credentials for demo purposes"""
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # Capture data for educational demonstration only
    captured_data.append({
        'username': username,
        'password': password,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ip': request.remote_addr
    })
    
    # Redirect to educational page
    return redirect(url_for('educational'))

@app.route('/educational')
def educational():
    """Educational page explaining the phishing demo"""
    return render_template('educational.html')

@app.route('/admin')
def admin():
    """Admin page to view captured credentials (for educational demonstration only)"""
    # For a real demo, you might want to add password protection here
    demo_url = request.url_root
    return render_template('admin.html', captured_data=captured_data, demo_url=demo_url)

@app.route('/admin/clear')
def clear_data():
    """Clear all captured data"""
    global captured_data
    captured_data = []
    return redirect(url_for('admin'))

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

def main():
    """Main function to run the phishing demo server"""
    # Setup the HTML files
    setup_html_files()
    
    # Get server IP and port
    host = '0.0.0.0'  # This makes the server accessible from other devices on the network
    port = 5000
    
    # Generate QR code for easier access from mobile devices
    server_url = f"http://{host}:{port}"
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        server_url = f"http://{local_ip}:{port}"
    except:
        pass
    
    generate_qr_code(server_url)
    
    print(f"=" * 70)
    print(f"EDUCATIONAL PHISHING DEMO SERVER")
    print(f"=" * 70)
    print(f"WARNING: This is for educational purposes only.")
    print(f"Server running at: {server_url}")
    print(f"QR Code generated at: static/qr_code.png")
    print(f"Admin page: {server_url}/admin")
    print(f"=" * 70)
    
    # Run the Flask app
    app.run(host=host, port=port, debug=True)

if __name__ == "__main__":
    main()