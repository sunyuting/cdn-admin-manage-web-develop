
from flask import Flask, request, jsonify
from flask_cors import CORS  # Importing CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)
# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'admin123',  # Replace with your MySQL password
    'database': 'user_db'
}

def create_connection():
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return conn

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')  # In a real app, ensure the password is hashed
    email = data.get('email')
    phone = data.get('phone')

    # Handle nullable fields
    email = email if email else None
    phone = phone if phone else None

    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            query = "INSERT INTO users (username, password, email, phone) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (username, password, email, phone))
            conn.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except Error as e:
            print(f"Error: {e}")
            return jsonify({'message': 'User already exists or invalid data'}), 400
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'message': 'Database connection failed'}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            if user:
                return jsonify({'message': 'Login successful', 'user': user}), 200
            else:
                return jsonify({'message': 'Invalid username or password'}), 401
        except Error as e:
            print(f"Error: {e}")
            return jsonify({'message': 'Login error'}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'message': 'Database connection failed'}), 500

@app.route('/reset-password', methods=['POST'])
def reset_password():
    print("Reset password route called") 
    data = request.json
    username = data.get('username')
    new_password = data.get('new_password')  # This should be generated or obtained securely

    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
            if cursor.rowcount == 0:
                return jsonify({'message': 'User not found'}), 404
            conn.commit()
            return jsonify({'message': 'Password reset successful'}), 200
        except Error as e:
            print(f"Error: {e}")
            return jsonify({'message': 'Password reset error'}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'message': 'Database connection failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
