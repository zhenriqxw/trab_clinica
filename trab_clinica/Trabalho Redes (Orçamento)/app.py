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
    cursor.execute("SELECT * FROM equipment")
    equipments = cursor.fetchall()
    total_value = sum(equipment['quantity'] * equipment['value'] for equipment in equipments)
    return render_template('index.html', equipments=equipments, total_value=total_value)

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
def add_equipment():
    if not check_logged_in():
        return redirect(url_for('login'))
    if request.method == 'POST':
        equipment = {
            'name': request.form['name'],
            'description': request.form['description'],
            'model': request.form['model'],
            'quantity': int(request.form['quantity']),
            'unit': request.form['unit'],
            'value': float(request.form['value']),
            'research_link': request.form['research_link']
        }
        cursor = db.cursor()
        cursor.execute("INSERT INTO equipment (name, description, model, quantity, unit, value, research_link) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                        (equipment['name'], equipment['description'], equipment['model'], equipment['quantity'], equipment['unit'], equipment['value'], equipment['research_link']))
        db.commit()
        return redirect(url_for('index'))
    return render_template('add_equipment.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_equipment(id):
    if not check_logged_in():
        return redirect(url_for('login'))
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        equipment = {
            'name': request.form['name'],
            'description': request.form['description'],
            'model': request.form['model'],
            'quantity': int(request.form['quantity']),
            'unit': request.form['unit'],
            'value': float(request.form['value']),
            'research_link': request.form['research_link']
        }
        cursor.execute("UPDATE equipment SET name = %s, description = %s, model = %s, quantity = %s, unit = %s, value = %s, research_link = %s WHERE id = %s",
                        (equipment['name'], equipment['description'], equipment['model'], equipment['quantity'], equipment['unit'], equipment['value'], equipment['research_link'], id))
        db.commit()
        return redirect(url_for('index'))
    cursor.execute("SELECT * FROM equipment WHERE id = %s", (id,))
    equipment = cursor.fetchone()
    return render_template('edit_equipment.html', equipment=equipment)

@app.route('/delete/<int:id>')
def delete_equipment(id):
    if not check_logged_in():
        return redirect(url_for('login'))
    cursor = db.cursor()
    cursor.execute("DELETE FROM equipment WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/login_error')
def login_error():
    return render_template('login_error.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
