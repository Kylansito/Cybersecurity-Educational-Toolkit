"""
SQL Injection Demonstration for Cybersecurity Education
------------------------------------------------------
This code demonstrates:
1. A vulnerable web application with SQL injection
2. An attack that exploits the vulnerability 
3. A secure version that prevents SQL injection
"""

import sqlite3
import flask
from flask import Flask, request, render_template_string, g

# Initialize Flask application
app = Flask(__name__)

# Database setup
def init_db():
    """Create a simple database with a users table"""
    conn = sqlite3.connect('demo.db')
    cursor = conn.cursor()
    
    # Drop table if it exists
    cursor.execute("DROP TABLE IF EXISTS users")
    
    # Create users table
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )""")
    
    # Insert sample users
    sample_users = [
        (1, 'admin', '£a;95}/ey4he6V%pKi}N$', 'administrator'),
        (2, 'alice', 'B[+Hr9nSroAQ280vl3SZ#', 'user'),
        (3, 'bob', 'tihYx0],xG27#VSl+F\,;', 'user'),
        (4, 'eve', 'm0.~vB6D\BH:I8i,$2_u2', 'user')
    ]
    
    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", sample_users)
    conn.commit()
    conn.close()
    print("Database initialized with sample data.")


def get_db():
    """Get database connection"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('demo.db')
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Close database connection when app context ends"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Basic HTML template for our demonstration
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SQL Injection Demo</title>
    <style>
        :root {
            --primary-color: #4361ee;
            --danger-color: #ef476f;
            --success-color: #06d6a0;
            --dark-color: #242424;
            --light-color: #f8f9fa;
            --gray-color: #e9ecef;
            --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            --transition: all 0.3s ease;
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--dark-color);
            background-color: #f0f2f5;
            margin: 0;
            padding: 0;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        header {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
            background-color: white;
            border-radius: 8px;
            box-shadow: var(--card-shadow);
        }
        
        h1 {
            color: var(--primary-color);
            margin-bottom: 0.5rem;
            font-weight: 700;
        }
        
        h2 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        h3 {
            font-size: 1.2rem;
            margin: 1rem 0;
            color: var(--dark-color);
        }
        
        .card {
            background-color: white;
            border-radius: 8px;
            box-shadow: var(--card-shadow);
            margin-bottom: 2rem;
            overflow: hidden;
            transition: var(--transition);
        }
        
        .card:hover {
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        }
        
        .card-header {
            padding: 1rem;
            border-bottom: 1px solid var(--gray-color);
        }
        
        .vulnerable .card-header {
            background-color: #fff5f7;
            border-left: 4px solid var(--danger-color);
        }
        
        .secure .card-header {
            background-color: #f0fff4;
            border-left: 4px solid var(--success-color);
        }
        
        .card-body {
            padding: 1.5rem;
        }
        
        form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        label {
            font-weight: 600;
            color: #4a5568;
        }
        
        input[type="text"] {
            padding: 0.75rem 1rem;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            font-size: 1rem;
            transition: var(--transition);
            width: 100%;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.25);
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 4px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
        }
        
        .btn-vulnerable {
            background-color: var(--danger-color);
            color: white;
        }
        
        .btn-vulnerable:hover {
            background-color: #d64161;
        }
        
        .btn-secure {
            background-color: var(--success-color);
            color: white;
        }
        
        .btn-secure:hover {
            background-color: #05b384;
        }
        
        .result-section {
            margin-top: 1.5rem;
            border-top: 1px solid var(--gray-color);
            padding-top: 1.5rem;
        }
        
        .query-display {
            background-color: var(--light-color);
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 1rem;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            border-left: 3px solid var(--primary-color);
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1rem 0;
            border-radius: 4px;
            overflow: hidden;
        }
        
        th, td {
            text-align: left;
            padding: 0.75rem 1rem;
        }
        
        th {
            background-color: var(--primary-color);
            color: white;
            font-weight: 600;
        }
        
        tr:nth-child(even) {
            background-color: var(--gray-color);
        }
        
        tr:hover {
            background-color: #e3e8f0;
        }
        
        .attack-examples {
            background-color: #fffbea;
            border-radius: 4px;
            padding: 1rem;
            margin-top: 1.5rem;
            border-left: 3px solid #f59f00;
        }
        
        .attack-examples h3 {
            color: #e67700;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .attack-examples h3:before {
            content: "⚠️";
        }
        
        .attack-list {
            list-style: none;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 0.75rem;
            margin-top: 1rem;
        }
        
        .attack-item {
            background-color: white;
            padding: 0.75rem;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }
        
        .attack-name {
            font-weight: 600;
            color: #4a5568;
            margin-right: 0.5rem;
        }
        
        code {
            background-color: #f1f5f9;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
        }
        
        .code-section {
            margin-top: 3rem;
        }
        
        .code-section h2 {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .code-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }
        
        @media (max-width: 768px) {
            .code-container {
                grid-template-columns: 1fr;
            }
        }
        
        .comparison-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }
        
        .code-card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .code-card:hover {
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        }
        
        .code-header {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .vulnerable .code-header {
            background-color: #fff5f7;
            border-left: 4px solid var(--danger-color);
        }
        
        .secure .code-header {
            background-color: #f0fff4;
            border-left: 4px solid var(--success-color);
        }
        
        .code-label {
            font-weight: 600;
            font-size: 1rem;
        }
        
        .code-content {
            padding: 1rem;
            background-color: #1a202c;
            color: #e2e8f0;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            line-height: 1.5;
            overflow-x: auto;
        }
        
        .code-line {
            white-space: pre;
            padding: 1px 0;
        }
        
        .indent {
            padding-left: 2rem;
        }
        
        .indent2 {
            padding-left: 4rem;
        }
        
        .highlight-danger {
            background-color: rgba(255, 71, 111, 0.2);
            border-left: 3px solid var(--danger-color);
            margin-left: -3px;
            padding-left: calc(2rem - 3px);
        }
        
        .highlight-success {
            background-color: rgba(6, 214, 160, 0.2);
            border-left: 3px solid var(--success-color);
            margin-left: -3px;
            padding-left: calc(2rem - 3px);
        }
        
        .keyword {
            color: #63b3ed;
        }
        
        .function {
            color: #90cdf4;
        }
        
        .decorator {
            color: #d6bcfa;
        }
        
        .string {
            color: #9ae6b4;
        }
        
        .comment {
            color: #718096;
        }
        
        .footer {
            text-align: center;
            margin-top: 2rem;
            padding: 1rem;
            color: #718096;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>SQL Injection Demonstration</h1>
            <p>Educational tool for understanding SQL injection vulnerabilities and prevention techniques</p>
        </header>
        
        <div class="card vulnerable">
            <div class="card-header">
                <h2>🔴 Vulnerable Login</h2>
            </div>
            <div class="card-body">
                <form method="POST" action="/vulnerable_login">
                    <div class="form-group">
                        <label for="vuln-username">Username:</label>
                        <input type="text" id="vuln-username" name="username" required placeholder="Enter username">
                    </div>
                    <div class="form-group">
                        <label for="vuln-password">Password:</label>
                        <input type="text" id="vuln-password" name="password" required placeholder="Enter password">
                    </div>
                    <button type="submit" class="btn btn-vulnerable">Login (Vulnerable)</button>
                </form>
                
                {% if vuln_result %}
                <div class="result-section">
                    <h3>Query Executed:</h3>
                    <div class="query-display">{{ vuln_query }}</div>
                    
                    <h3>Result:</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Username</th>
                                <th>Password</th>
                                <th>Role</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for row in vuln_result %}
                            <tr>
                                <td>{{ row[0] }}</td>
                                <td>{{ row[1] }}</td>
                                <td>{{ row[2] }}</td>
                                <td>{{ row[3] }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% endif %}
                
                <div class="attack-examples">
                    <h3>Try these attack patterns</h3>
                    <div class="attack-list">
                        <div class="attack-item">
                            <span class="attack-name">Basic Authentication Bypass:</span>
                            <div>Username: <code>admin' --</code></div>
                            <div>Password: <code>anything</code></div>
                        </div>
                        <div class="attack-item">
                            <span class="attack-name">Always True Condition:</span>
                            <div>Username: <code>' OR '1'='1</code></div>
                            <div>Password: <code>' OR '1'='1</code></div>
                        </div>
                        <div class="attack-item">
                            <span class="attack-name">Admin Login Bypass:</span>
                            <div>Username: <code>admin' OR 1=1 --</code></div>
                            <div>Password: <code>anything</code></div>
                        </div>
                        <div class="attack-item">
                            <span class="attack-name">Destructive Attack:</span>
                            <div>Username: <code>admin'; DROP TABLE users; --</code></div>
                            <div>Password: <code>anything</code></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card secure">
            <div class="card-header">
                <h2>🟢 Secure Login (Parameterized Queries)</h2>
            </div>
            <div class="card-body">
                <form method="POST" action="/secure_login">
                    <div class="form-group">
                        <label for="secure-username">Username:</label>
                        <input type="text" id="secure-username" name="username" required placeholder="Enter username">
                    </div>
                    <div class="form-group">
                        <label for="secure-password">Password:</label>
                        <input type="text" id="secure-password" name="password" required placeholder="Enter password">
                    </div>
                    <button type="submit" class="btn btn-secure">Login (Secure)</button>
                </form>
                
                {% if secure_result %}
                <div class="result-section">
                    <h3>Query Executed:</h3>
                    <div class="query-display">{{ secure_query }}</div>
                    
                    <h3>Result:</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Username</th>
                                <th>Password</th>
                                <th>Role</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for row in secure_result %}
                            <tr>
                                <td>{{ row[0] }}</td>
                                <td>{{ row[1] }}</td>
                                <td>{{ row[2] }}</td>
                                <td>{{ row[3] }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% endif %}
            </div>
        </div>
        
        <div class="code-section">
            <h2>Source Code Comparison</h2>
            <div class="comparison-container">
                <div class="code-card vulnerable">
                    <div class="code-header">
                        <span class="code-label">❌ Vulnerable Code</span>
                    </div>
                    <div class="code-content">
                        <div class="code-line"><span class="decorator">@app.route</span>(<span class="string">'/vulnerable_login'</span>, methods=[<span class="string">'POST'</span>])</div>
                        <div class="code-line"><span class="keyword">def</span> <span class="function">vulnerable_login</span>():</div>
                        <div class="code-line indent">username = request.form[<span class="string">'username'</span>]</div>
                        <div class="code-line indent">password = request.form[<span class="string">'password'</span>]</div>
                        <div class="code-line indent"></div>
                        <div class="code-line indent"><span class="comment"># VULNERABLE: Direct string concatenation in SQL query</span></div>
                        <div class="code-line indent highlight-danger">query = <span class="string">f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"</span></div>
                        <div class="code-line indent"></div>
                        <div class="code-line indent"><span class="comment"># Execute the query</span></div>
                        <div class="code-line indent">conn = get_db()</div>
                        <div class="code-line indent">cursor = conn.cursor()</div>
                        <div class="code-line indent">cursor.execute(query)</div>
                        <div class="code-line indent">result = cursor.fetchall()</div>
                        <div class="code-line indent"></div>
                        <div class="code-line indent"><span class="keyword">return</span> render_template_string(HTML_TEMPLATE,</div>
                        <div class="code-line indent2">vuln_result=result,</div>
                        <div class="code-line indent2">vuln_query=query)</div>
                    </div>
                </div>
                
                <div class="code-card secure">
                    <div class="code-header">
                        <span class="code-label">✅ Secure Code</span>
                    </div>
                    <div class="code-content">
                        <div class="code-line"><span class="decorator">@app.route</span>(<span class="string">'/secure_login'</span>, methods=[<span class="string">'POST'</span>])</div>
                        <div class="code-line"><span class="keyword">def</span> <span class="function">secure_login</span>():</div>
                        <div class="code-line indent">username = request.form[<span class="string">'username'</span>]</div>
                        <div class="code-line indent">password = request.form[<span class="string">'password'</span>]</div>
                        <div class="code-line indent"></div>
                        <div class="code-line indent"><span class="comment"># SECURE: Use parameterized queries</span></div>
                        <div class="code-line indent highlight-success">query = <span class="string">"SELECT * FROM users WHERE username = ? AND password = ?"</span></div>
                        <div class="code-line indent highlight-success">display_query = <span class="string">f"SELECT * FROM users WHERE username = ? AND password = ?"</span></div>
                        <div class="code-line indent"></div>
                        <div class="code-line indent"><span class="comment"># Execute with parameters</span></div>
                        <div class="code-line indent">conn = get_db()</div>
                        <div class="code-line indent">cursor = conn.cursor()</div>
                        <div class="code-line indent highlight-success">cursor.execute(query, (username, password))</div>
                        <div class="code-line indent">result = cursor.fetchall()</div>
                        <div class="code-line indent"></div>
                        <div class="code-line indent"><span class="keyword">return</span> render_template_string(HTML_TEMPLATE,</div>
                        <div class="code-line indent2">secure_result=result,</div>
                        <div class="code-line indent2">secure_query=display_query)</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>SQL Injection Demonstration Tool for Educational Purposes Only</p>
        </div>
    </div>
</body>
</html>
"""

# Routes definitions
@app.route('/')
def index():
    """Main page with both vulnerable and secure login forms"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/vulnerable_login', methods=['POST'])
def vulnerable_login():
    """Vulnerable login implementation using string concatenation"""
    username = request.form['username']
    password = request.form['password']
    
    # VULNERABLE: Direct string concatenation in SQL query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    # Execute the vulnerable query
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except sqlite3.Error as e:
        result = []
        query = f"{query} (ERROR: {str(e)})"
    
    return render_template_string(HTML_TEMPLATE, 
                                 vuln_result=result,
                                 vuln_query=query)


@app.route('/secure_login', methods=['POST'])
def secure_login():
    """Secure login implementation using parameterized queries"""
    username = request.form['username']
    password = request.form['password']
    
    # SECURE: Use parameterized queries / prepared statements
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    display_query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}' (Executed with parameters)" 
    
    # Execute the secure query with parameters
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, (username, password))
    result = cursor.fetchall()
    
    return render_template_string(HTML_TEMPLATE, 
                                 secure_result=result,
                                 secure_query=display_query)


if __name__ == '__main__':
    # Initialize database before starting
    init_db()
    
    # Start the Flask application
    print("Starting SQL Injection Demo Server...")
    print("Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True)