from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
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

def initialize_database():
    if programs_collection.count_documents({}) == 0:
        # Data contoh untuk koleksi programs
        programs = [
            {"name": "Program Pemberdayaan Pemuda", "location": "Jakarta", "participants": 120, "budget": 25000, "status": "Active"},
            {"name": "Pelatihan Keterampilan Digital", "location": "Bandung", "participants": 80, "budget": 15000, "status": "Active"},
            {"name": "Workshop Pengembangan Karir", "location": "Surabaya", "participants": 40, "budget": 7000, "status": "Inactive"},
            {"name": "Seminar Pendidikan Global", "location": "Medan", "participants": 200, "budget": 30000, "status": "Active"},
            {"name": "Program Akses Pendidikan untuk Anak-anak", "location": "Yogyakarta", "participants": 100, "budget": 18000, "status": "Inactive"},
            {"name": "Kursus Bahasa Asing untuk Profesional", "location": "Bali", "participants": 150, "budget": 22000, "status": "Active"},
            {"name": "Pelatihan Guru Terpadu", "location": "Makassar", "participants": 60, "budget": 13000, "status": "Inactive"},
            {"name": "Program Magang Profesional", "location": "Medan", "participants": 110, "budget": 25000, "status": "Active"},
            {"name": "Kursus Pengembangan Teknologi Informasi", "location": "Jakarta", "participants": 75, "budget": 16000, "status": "Active"},
            {"name": "Forum Pendidikan dan Pengembangan Sosial", "location": "Bandung", "participants": 50, "budget": 12000, "status": "Inactive"},
            {"name": "Pelatihan Kepemimpinan di Dunia Kerja", "location": "Solo", "participants": 90, "budget": 20000, "status": "Active"},
            {"name": "Pemberdayaan Komunitas Melalui Pendidikan", "location": "Bali", "participants": 65, "budget": 14000, "status": "Inactive"},
            {"name": "Program Beasiswa untuk Pelajar Berprestasi", "location": "Yogyakarta", "participants": 100, "budget": 25000, "status": "Active"}
        ]
        programs_collection.insert_many(programs)  # Menyisipkan semua program
        print("Database initialized with programs.")

# Inisialisasi database sebelum aplikasi berjalan
initialize_database()

@app.route('/get_program_data', methods=['GET'])
def get_program_data():
    programs = list(programs_collection.find({}, {"_id": 0}))  # Exclude '_id'
    return jsonify(programs)

# **Route baru untuk mendapatkan data artikel**
@app.route('/get_artikel_data', methods=['GET'])
def get_artikel_data():
    programs = list(programs_collection.find({}, {"_id": 0}))  # Exclude '_id'
    return jsonify(programs)

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
