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
category_collection = db["category"]

# Inisialisasi database dengan detail berupa timeline atau deskripsi proyek
def initialize_database():
    if programs_collection.count_documents({}) == 0:
        # Data contoh untuk koleksi programs dengan tambahan kolom 'detail' (deskripsi atau timeline)
        programs = [
            {
                "name": "Program Pemberdayaan Pemuda", 
                "location": "Jakarta", 
                "participants": 120, 
                "budget": 25000,
                "category": "Perguruan Tinggi",
                "status": "Sedang Berlangsung", 
                "detail": """
                    1. Minggu 1-2: Rekrutmen peserta dan pelatihan dasar tentang keterampilan kepemimpinan.
                    2. Minggu 3-4: Pengembangan keterampilan teknis (seperti programming, desain grafis, dll.).
                    3. Minggu 5-6: Workshop tentang pengembangan karir dan kewirausahaan.
                    4. Minggu 7-8: Penyuluhan tentang kesehatan mental dan pengembangan pribadi.
                    5. Minggu 9: Penilaian akhir dan presentasi hasil pelatihan oleh peserta.
                    Program ini bertujuan untuk memberdayakan pemuda dengan keterampilan dan pengetahuan yang dapat meningkatkan kualitas hidup mereka di masa depan.
                """
            },
            {
                "name": "Pelatihan Keterampilan Digital", 
                "location": "Bandung", 
                "participants": 80, 
                "budget": 15000, 
                "category": "Perguruan Tinggi",
                "status": "Sedang Berlangsung", 
                "detail": """
                    1. Minggu 1-2: Pengenalan alat dan perangkat lunak yang digunakan dalam keterampilan digital.
                    2. Minggu 3-4: Pelatihan dalam desain grafis menggunakan Adobe Photoshop dan Illustrator.
                    3. Minggu 5-6: Pelatihan dalam pengembangan website menggunakan HTML, CSS, dan JavaScript.
                    4. Minggu 7: Simulasi dan tugas akhir untuk mengembangkan sebuah proyek digital.
                    5. Minggu 8: Penyelesaian dan presentasi proyek akhir kepada penguji dan mentor.
                    Pelatihan ini bertujuan memberikan keterampilan digital yang dibutuhkan oleh para peserta untuk mempersiapkan mereka menghadapi tantangan dunia kerja digital.
                """
            },
            {
                "name": "Workshop Pengembangan Karir", 
                "location": "Surabaya", 
                "participants": 40, 
                "budget": 7000, 
                "category": "Perguruan Tinggi",
                "status": "Selesai", 
                "detail": """
                    1. Hari 1: Sesi pengenalan tentang dunia kerja dan persiapan karir.
                    2. Hari 2-3: Diskusi panel dengan profesional dari berbagai industri.
                    3. Hari 4-5: Pelatihan keterampilan komunikasi dan presentasi yang efektif.
                    4. Hari 6: Workshop penulisan CV dan surat lamaran kerja yang menonjol.
                    5. Hari 7: Simulasi wawancara kerja dan evaluasi oleh para ahli.
                    Workshop ini membantu peserta merencanakan dan mengembangkan karir mereka dengan keterampilan yang dibutuhkan dalam dunia kerja.
                """
            },
            {
                "name": "Seminar Pendidikan Global", 
                "location": "Medan", 
                "participants": 200, 
                "budget": 30000, 
                "category": "Perguruan Tinggi",
                "status": "Sedang Berlangsung", 
                "detail": """
                    1. Sesi 1: Pengenalan mengenai perkembangan pendidikan di berbagai belahan dunia.
                    2. Sesi 2: Pembahasan tentang tantangan yang dihadapi oleh sistem pendidikan global.
                    3. Sesi 3: Inovasi dalam pendidikan: teknologi, metode baru, dan pembelajaran berbasis kompetensi.
                    4. Sesi 4: Diskusi kelompok tentang solusi untuk meningkatkan kualitas pendidikan secara global.
                    5. Penutupan: Presentasi ide dan solusi oleh peserta seminar.
                    Seminar ini bertujuan untuk membahas isu-isu terkini dalam dunia pendidikan dan mengidentifikasi solusi untuk memperbaikinya di tingkat global.
                """
            },
            {
                "name": "Program Akses Pendidikan untuk Anak-anak", 
                "location": "Yogyakarta", 
                "participants": 100, 
                "budget": 18000, 
                "category": "Umum",
                "status": "Selesai", 
                "detail": """
                    1. Minggu 1: Pengenalan kepada anak-anak mengenai pentingnya pendidikan.
                    2. Minggu 2-4: Penyuluhan kepada orang tua mengenai akses pendidikan bagi anak-anak.
                    3. Minggu 5-7: Pemberian materi pendidikan dasar berupa keterampilan membaca, menulis, dan berhitung.
                    4. Minggu 8: Evaluasi belajar dan pembagian sertifikat kepada anak-anak.
                    Program ini bertujuan untuk memberikan kesempatan kepada anak-anak dari keluarga kurang mampu agar dapat mengakses pendidikan yang berkualitas.
                """
            },
            {
                "name": "Kursus Bahasa Asing untuk Profesional", 
                "location": "Bali", 
                "participants": 150, 
                "budget": 22000, 
                "category": "Umum",
                "status": "Sedang Berlangsung", 
                "detail": """
                    1. Minggu 1-2: Pelatihan dasar bahasa Inggris untuk komunikasi profesional.
                    2. Minggu 3-5: Pelatihan bahasa Mandarin untuk kebutuhan internasional.
                    3. Minggu 6-8: Pelatihan bahasa Jepang untuk industri teknologi dan otomotif.
                    4. Minggu 9: Penyuluhan tentang budaya dan etiket komunikasi profesional.
                    Kursus ini membantu para profesional memperluas wawasan dan keterampilan bahasa untuk memperluas jaringan internasional.
                """
            },
            {
                "name": "Pelatihan Guru Terpadu", 
                "location": "Makassar", 
                "participants": 60, 
                "budget": 13000, 
                "category": "Perguruan Tinggi",
                "status": "Selesai", 
                "detail": """
                    1. Minggu 1-3: Pelatihan tentang metode pembelajaran interaktif dan kreatif.
                    2. Minggu 4-6: Pelatihan penggunaan teknologi dalam pembelajaran digital.
                    3. Minggu 7-8: Pengembangan keterampilan komunikasi dan manajemen kelas yang efektif.
                    4. Minggu 9: Penyuluhan mengenai kesejahteraan mental dan emosional guru.
                    Pelatihan ini bertujuan untuk meningkatkan kualitas pengajaran dan kesejahteraan guru di seluruh wilayah.
                """
            },
            {
                "name": "Program Magang Profesional", 
                "location": "Medan", 
                "participants": 110, 
                "budget": 25000, 
                "category": "Perguruan Tinggi",
                "status": "Sedaang Berlangsung", 
                "detail": """
                    1. Minggu 1: Orientasi dan pengenalan lingkungan kerja di berbagai perusahaan.
                    2. Minggu 2-4: Penugasan praktis dengan bimbingan dari mentor profesional.
                    3. Minggu 5-7: Pengerjaan proyek nyata yang terkait dengan bidang studi peserta.
                    4. Minggu 8: Evaluasi dan laporan akhir mengenai pengalaman magang.
                    Program ini bertujuan untuk memberi kesempatan bagi mahasiswa untuk merasakan langsung dunia kerja dan memperkaya pengalaman profesional mereka.
                """
            },
            {
                "name": "Kursus Pengembangan Teknologi Informasi", 
                "location": "Jakarta", 
                "participants": 75, 
                "budget": 16000, 
                "category": "SMA",
                "status": "Sedang Berlangsung", 
                "detail": """
                    1. Minggu 1-2: Pengantar pengembangan perangkat lunak dan dasar-dasar pemrograman.
                    2. Minggu 3-5: Pelatihan lanjutan dalam bahasa pemrograman seperti Python dan Java.
                    3. Minggu 6-8: Pengembangan aplikasi berbasis web menggunakan HTML, CSS, dan JavaScript.
                    4. Minggu 9: Penyelesaian proyek akhir dalam pengembangan aplikasi.
                    Kursus ini bertujuan untuk memperkenalkan dan mengembangkan keterampilan dalam bidang teknologi informasi bagi para peserta.
                """
            },
            {
                "name": "Forum Pendidikan dan Pengembangan Sosial", 
                "location": "Bandung", 
                "participants": 50, 
                "budget": 12000, 
                "category": "Umum",
                "status": "Selesai", 
                "detail": """
                    1. Hari 1: Diskusi mengenai isu sosial terkini yang mempengaruhi dunia pendidikan.
                    2. Hari 2: Presentasi oleh ahli pendidikan mengenai inovasi dalam sistem pendidikan.
                    3. Hari 3: Workshop mengenai pengembangan sosial dan pemberdayaan masyarakat.
                    4. Hari 4: Rencana aksi dan evaluasi mengenai langkah-langkah pengembangan sosial.
                    Forum ini bertujuan untuk memberikan wawasan kepada peserta mengenai tantangan pendidikan dan bagaimana memecahkannya.
                """
            },
            {
                "name": "Pelatihan Kepemimpinan di Dunia Kerja", 
                "location": "Solo", 
                "participants": 90, 
                "budget": 20000, 
                "category": "Umum",
                "status": "Sedaang Berlangsung", 
                "detail": """
                    1. Minggu 1-2: Pengenalan kepada konsep kepemimpinan yang efektif.
                    2. Minggu 3-4: Pelatihan tentang pengambilan keputusan dan pemecahan masalah.
                    3. Minggu 5-6: Workshop komunikasi dan negosiasi untuk kepemimpinan.
                    4. Minggu 7-8: Simulasi kepemimpinan dan penilaian dari mentor.
                    Program ini bertujuan untuk melatih keterampilan kepemimpinan peserta agar siap menghadapi tantangan di dunia kerja.
                """
            },
            {
                "name": "Pemberdayaan Komunitas Melalui Pendidikan", 
                "location": "Bali", 
                "participants": 65, 
                "budget": 14000, 
                "category": "Umum",
                "status": "Selesai", 
                "detail": """
                    1. Minggu 1: Pengenalan tentang pentingnya pendidikan di tingkat komunitas.
                    2. Minggu 2-4: Program pelatihan keterampilan dasar untuk masyarakat setempat.
                    3. Minggu 5-7: Penyuluhan tentang pengelolaan sumber daya alam dan pengentasan kemiskinan.
                    4. Minggu 8: Pemberian sertifikat kepada peserta yang berhasil.
                    Program ini bertujuan untuk memberdayakan komunitas lokal dengan pendidikan yang relevan dan bermanfaat.
                """
            },
            {
                "name": "Program Beasiswa untuk Pelajar Berprestasi", 
                "location": "Yogyakarta", 
                "participants": 100, 
                "budget": 25000, 
                "category": "SMP",
                "status": "Sedang Berlangsung", 
                "detail": """
                    1. Minggu 1: Seleksi penerima beasiswa berdasarkan prestasi akademik dan non-akademik.
                    2. Minggu 2-4: Pelatihan untuk membantu peserta beasiswa dalam mencapai tujuan akademik mereka.
                    3. Minggu 5-7: Program mentoring oleh alumni beasiswa untuk pembinaan.
                    4. Minggu 8: Penyerahan beasiswa dan laporan pencapaian.
                    Program ini bertujuan untuk memberi kesempatan bagi pelajar berprestasi yang membutuhkan dukungan finansial untuk melanjutkan pendidikan mereka.
                """
            },
            {
        "name": "Pelatihan Startup Digital untuk Wirausahawan Muda",
        "location": "Jakarta",
        "participants": 50,
        "budget": 20000,
        "category": "Perguruan Tinggi",
        "status": "Coming Soon",
        "detail": """
            1. Hari 1: Pengantar tentang startup digital dan tren pasar global.
            2. Hari 2-3: Workshop membangun model bisnis menggunakan Business Model Canvas (BMC).
            3. Hari 4: Sesi mentoring dengan pengusaha sukses untuk berbagi pengalaman.
            4. Hari 5-6: Pelatihan pengembangan produk minimum yang layak (MVP).
            5. Hari 7: Pitching ide bisnis di depan panel investor dan mentor.
            Program ini memberikan pemahaman menyeluruh tentang proses membangun dan mengembangkan startup digital.
        """
    },
    {
        "name": "Kampanye Lingkungan dan Penanaman Pohon",
        "location": "Bandung",
        "participants": 150,
        "budget": 12000,
        "category": "Umum",
        "status": "Coming Soon",
        "detail": """
            1. Hari 1: Pengenalan tentang dampak perubahan iklim dan pentingnya penghijauan.
            2. Hari 2: Diskusi kelompok tentang cara menjaga lingkungan dan solusi lokal.
            3. Hari 3: Kegiatan penanaman 500 pohon di kawasan konservasi lokal.
            4. Hari 4: Sesi dokumentasi dan promosi kampanye di media sosial.
            5. Hari 5: Evaluasi hasil program dan perencanaan kampanye lanjutan.
            Kampanye ini bertujuan untuk meningkatkan kesadaran masyarakat tentang pentingnya menjaga lingkungan.
        """
    },
    {
        "name": "Program Peningkatan Literasi Digital untuk Orang Tua",
        "location": "Yogyakarta",
        "participants": 80,
        "budget": 18000,
        "category": "Umum",
        "status": "Coming Soon",
        "detail": """
            1. Minggu 1: Dasar-dasar penggunaan perangkat digital seperti smartphone dan laptop.
            2. Minggu 2: Pelatihan penggunaan aplikasi komunikasi seperti WhatsApp dan Zoom.
            3. Minggu 3: Keamanan digital, termasuk mengenali phishing dan menjaga privasi online.
            4. Minggu 4: Akses sumber daya pendidikan online untuk membantu anak belajar.
            5. Minggu 5: Praktik langsung dalam mengelola aktivitas online keluarga.
            Program ini bertujuan untuk memberdayakan orang tua agar lebih percaya diri dalam mendukung pendidikan anak di era digital.
        """
    }
        ]
        programs_collection.insert_many(programs)  # Menyisipkan semua program
        print("Database initialized with programs and detailed descriptions.")

    if category_collection.count_documents({}) == 0:
        category = [
            {"name": "TK"},
            {"name": "SD"},
            {"name": "SMP"},
            {"name": "SMA"},
            {"name": "SMK"},
            {"name": "Perguruan Tinggi"},
            {"name": "Umum"}
        ]
        category_collection.insert_many(category)  # Menyisipkan semua kategori
        print("Database initialized with categories.")

# Inisialisasi database sebelum aplikasi berjalan
initialize_database()

@app.route('/get_program_data', methods=['GET'])
def get_program_data():
    programs = list(programs_collection.find({}, {"_id": 0}))  # Exclude '_id'
    return jsonify(programs)

# Route baru untuk mendapatkan data artikel
@app.route('/get_artikel_data', methods=['GET'])
def get_artikel_data():
    programs = list(programs_collection.find({}, {"_id": 0}))  # Exclude '_id'
    return jsonify(programs)

# Halaman Utama (Home)
@app.route('/')
def home():
    programs = programs_collection.find()
    # Cek apakah user sudah login
    username = session.get("username")
    return render_template('home.html', username=username)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Cek jika username ada di database
        user = users_collection.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password", "danger")
    
    return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        full_name = request.form["full_name"]  # New field
        workplace = request.form["workplace"]  # New field

        # Cek apakah email sudah terdaftar
        if users_collection.find_one({"email": email}):
            flash("Email is already registered!", "danger")
            return redirect(url_for('register'))

        # Cek apakah username sudah terdaftar
        if users_collection.find_one({"username": username}):
            flash("Username is already taken!", "danger")
            return redirect(url_for('register'))

        # Simpan pengguna baru jika tidak ada masalah
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({
            "email": email,
            "username": username,
            "password": hashed_password,
            "full_name": full_name,  # Save full_name
            "workplace": workplace   # Save workplace
        })
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/profile', methods=["GET", "POST"])
def profile():
    if "username" not in session:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for('login'))

    username = session["username"]
    user = users_collection.find_one({"username": username}, {"_id": 0})

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('login'))

    if request.method == "POST":
        full_name = request.form["full_name"]
        workplace = request.form["workplace"]

        users_collection.update_one(
            {"username": username},
            {"$set": {"full_name": full_name, "workplace": workplace}}
        )
        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile'))

    programs = programs_collection.find({"username": username})
    return render_template('profile.html', user=user, programs=programs)

@app.route('/delete_program/<program_id>', methods=["POST"])
def delete_program(program_id):
    if "username" not in session:
        flash("Please log in to perform this action.", "warning")
        return redirect(url_for('login'))

    result = programs_collection.delete_one({"_id": ObjectId(program_id)})
    if result.deleted_count > 0:
        flash("Program deleted successfully!", "success")
    else:
        flash("Program not found or could not be deleted.", "danger")

    return redirect(url_for('profile'))

@app.route('/create_program', methods=['GET', 'POST'])
def create_program():
    if request.method == 'POST':
        try:
            # Ambil username dari session
            username = session.get('username')
            if not username:
                flash('You must be logged in to create a program!')
                return redirect(url_for('login'))

            # Ambil data dari form
            program_name = request.form.get('programName', '').strip()
            detail = request.form.get('detail', '').strip()
            location = request.form.get('location', '').strip()
            participants = int(request.form.get('participants', 0))
            budget = float(request.form.get('budget', 0.0))
            start_date = request.form.get('startDate', '').strip()
            end_date = request.form.get('endDate', '').strip()
            status = request.form.get('status', '').strip()
            category = request.form.get('category', '').strip()

            # Validasi kategori ada
            if not category_collection.find_one({'name': category}):
                flash(f'Category "{category}" does not exist!')
                return redirect(url_for('create_program'))

            # Validasi data wajib
            if not (program_name and detail and location and start_date and end_date and status):
                flash('Please fill in all required fields!')
                return redirect(url_for('create_program'))

            # Persiapkan data untuk disimpan
            program_data = {
                "username": username,  # Tambahkan username untuk filter nanti
                "name": program_name,
                "detail": detail,
                "location": location,
                "participants": participants,
                "budget": budget,
                "start_date": start_date,
                "end_date": end_date,
                "status": status,
                "category": category,
            }

            # Masukkan ke database
            programs_collection.insert_one(program_data)
            flash('Program created successfully!')
            return redirect(url_for('profile'))

        except Exception as e:
            # Tangani error tak terduga
            flash(f'An error occurred: {str(e)}')
            return redirect(url_for('create_program'))

    # Ambil daftar kategori untuk dropdown
    categories = [cat['name'] for cat in category_collection.find()]
    return render_template('create_program.html', categories=categories)

@app.route('/update_program', methods=['GET', 'POST'])
def update_program():
    if request.method == 'POST':
        # Get form data
        program_id = request.form['programId']
        program_name = request.form['programName']
        description = request.form['description']
        location = request.form['location']
        participants = request.form['participants']
        budget = request.form['budget']
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        status = request.form['status']
        
        # Process the data (e.g., update in database)
        print("Program Updated:", {
            'program_id': program_id,
            'program_name': program_name,
            'description': description,
            'location': location,
            'participants': participants,
            'budget': budget,
            'start_date': start_date,
            'end_date': end_date,
            'status': status
        })
        
        flash('Program updated successfully!')
        return redirect(url_for('profile'))
    
    # Fetch program data for pre-population (example with mock data)
    program = {
        'id': 1,
        'name': 'Sample Program',
        'description': 'This is a sample description.',
        'location': 'Jakarta',
        'participants': 20,
        'budget': 5000000,
        'start_date': '2025-01-01',
        'end_date': '2025-01-10',
        'status': 'Ongoing'
    }
    return render_template('update_program.html', program=program)

# Logout
@app.route('/logout')
def logout():
    session.pop("username", None)  # Menghapus username dari session
    flash("Logged out successfully!", "info")
    return redirect(url_for('home'))

@app.route('/search', methods=['GET'])
def search():
    # Ambil parameter query dari input pengguna
    query = request.args.get('q', '').strip()  # Dapatkan query pencarian, hapus spasi tambahan
    search_filter = {}

    # Jika ada query, buat filter untuk pencarian
    if query:
        search_filter = {
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},      # Cari di kolom name
                {"location": {"$regex": query, "$options": "i"}},  # Cari di kolom location
                {"status": {"$regex": query, "$options": "i"}}     # Cari di kolom status
            ]
        }

    # Query ke database
    results = programs_collection.find(search_filter)

    # Kembalikan hasil sebagai JSON
    return jsonify([
        {
            "_id": str(result["_id"]),  # Konversi ObjectId ke string
            "name": result["name"],
            "location": result["location"],
            "status": result["status"],
            "participants": result["participants"],
            "budget": result["budget"],
            "detail": result["detail"]
        }
        for result in results
    ])


# Jalankan Aplikasi
if __name__ == "__main__":
    app.run(debug=True)
