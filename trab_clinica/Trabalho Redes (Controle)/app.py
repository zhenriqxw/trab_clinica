from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port=3306,
    database="rack_management"
)

def check_logged_in():
    return 'logged_in' in session

@app.route('/')
def index():
    if not check_logged_in():
        return redirect(url_for('login'))
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM connections")
    connections = cursor.fetchall()
    return render_template('index.html', connections=connections)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM funcionarios WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error_message = "Usuário ou senha incorretos. Tente novamente."

    return render_template('login.html', error_message=error_message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM funcionarios WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            error_message = "Nome de usuário já existe!"
        else:
            cursor.execute("INSERT INTO funcionarios (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            return redirect(url_for('login'))

    return render_template('register.html', error_message=error_message)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add_connection():
    if not check_logged_in():
        return redirect(url_for('login'))
    if request.method == 'POST':
        switch_port = request.form['switch_port']
        patch_panel_port = request.form['patch_panel_port']
        cursor = db.cursor()
        cursor.execute("INSERT INTO connections (switch_port, patch_panel_port) VALUES (%s, %s)", (switch_port, patch_panel_port))
        db.commit()
        return redirect(url_for('index'))
    return render_template('add_connection.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_connection(id):
    if not check_logged_in():
        return redirect(url_for('login'))
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        switch_port = request.form['switch_port']
        patch_panel_port = request.form['patch_panel_port']
        cursor.execute("UPDATE connections SET switch_port = %s, patch_panel_port = %s WHERE id = %s", (switch_port, patch_panel_port, id))
        db.commit()
        return redirect(url_for('index'))
    cursor.execute("SELECT * FROM connections WHERE id = %s", (id,))
    connection = cursor.fetchone()
    return render_template('edit_connection.html', connection=connection)

@app.route('/delete/<int:id>')
def delete_connection(id):
    if not check_logged_in():
        return redirect(url_for('login'))
    cursor = db.cursor()
    cursor.execute("DELETE FROM connections WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
