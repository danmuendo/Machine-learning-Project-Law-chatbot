import hashlib
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
import processor



app = Flask(__name__)
app.config['SECRET_KEY']='secret'
app.static_folder = 'static'

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/")
def home():
    
    return render_template("login.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return processor.chatbot_response(userText)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password using hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if the username or email is already in use
        # conn = sqlite3.connect('database.db')
        
        # create a connection to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # create a table to store user information
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            );
        ''')

        
        # cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username=? OR email=?"
        cursor.execute(query, (username, email))
        existing_user = cursor.fetchone()
        

        if existing_user:
            # Show an error message
            error = "Username or email already in use"
            return render_template('login.html', error=error)
        else:
            # Insert the new user into the database
            insert_query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
            cursor.execute(insert_query, (username, email, hashed_password))
            conn.commit()

            # Show a success message
            success = "Registration successful"
            return redirect(url_for('index', success=success))

    # If the request method is GET, show the registration form
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password using hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if the username and hashed password match a record in the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username=? AND password=?"
        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()

        if user:
            # Store the user's ID in the session
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        else:
            # Show an error message
            error = "Invalid username or password"
            return redirect(url_for('login', error=error))

    # If the request method is GET, show the login form
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)