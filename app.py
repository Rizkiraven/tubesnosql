from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# Inisialisasi Flask
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Untuk flash messages

# Koneksi MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["education_db"]
users_collection = db["users"]
programs_collection = db["programs"]

# Halaman Utama (langsung bisa diakses tanpa login)
@app.route('/')
def home():
    programs = programs_collection.find()
    return render_template('home.html', programs=programs)

# Halaman Login
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = users_collection.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password", "danger")
    return render_template('login.html')

# Halaman Register
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Cek jika username sudah digunakan
        if users_collection.find_one({"username": username}):
            flash("Username already exists", "danger")
            return redirect(url_for('register'))
        
        # Simpan pengguna baru
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({"username": username, "password": hashed_password})
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

# Logout
@app.route('/logout')
def logout():
    session.pop("username", None)
    flash("Logged out successfully!", "info")
    return redirect(url_for('home'))

# Jalankan Aplikasi
if __name__ == "__main__":
    app.run(debug=True)
