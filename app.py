from flask import Flask, render_template, request, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import firebase_admin
from firebase_admin import credentials, firestore
from werkzeug.utils import redirect
from functools import wraps
import requests
from requests.structures import CaseInsensitiveDict

cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)
app.secret_key = 'wkwkwkwkwk'

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash('You have not login', 'danger')
            return redirect(url_for('login')) 
    return wrapper


def send_wa(m, p):
    api = "69eaa41b2ae7bcb3b3a9eebb30009849e3df97b1"
    url = "https://starsender.online/api/sendText"

    data = {
        "tujuan": "p",
        "message": "m"
    }

    headers = CaseInsensitiveDict()
    headers["apikey"] = api

    res = requests.post(url, json=data, headers=headers)


@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/tambah_data')
# def tambah_data():
#     data = {
#         "username": "mujibhasib",
#         "email": "mujib.hasib2294@gmail.com",
#         "jurusan": "Sistem Informasi"
#     }

#     db.collection("users").document().set(data)

#     return "berhasil"



# @app.route('/mahasiswa')
# def mahasiswa():
#     maba = db.collection("mahasiswa").stream()
#     mb = []

#     for mhs in maba:
#         m = mhs.to_dict()
#         mb.append(m)

#     return render_template('mahasiswa.html', data=mb)


@app.route('/mahasiswa')
@login_required
def mahasiswa():
    maba = db.collection("mahasiswa").stream()
    mb = []

    for mhs in maba:
        m = mhs.to_dict()
        m["id"] = mhs.id
        mb.append(m)

    return render_template('mahasiswa.html', data=mb)

@app.route('/mahasiswa/tambah', methods = ["GET", "POST"])
def tambah_mhs():
    if request.method == 'POST':
        data = {
            "nama": request.form["nama"],
            "email": request.form["email"],
            "nim": request.form["nim"],
            "jurusan": request.form["jurusan"]
        }
# ini adalah fungsi firebase untuk menambahkan data
        db.collection("mahasiswa").document().set(data)
        flash("student has been added", "success")
        return redirect(url_for('mahasiswa'))
    return render_template('add_mhs.html')
        



@app.route('/register', methods = ["GET", "POST"])
def register():
    # cek dulu methodnya
    if request.method == "POST":
    # if post
        # ambil data dari form
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "number": request.form["number"]
        }
        users = db.collection('users').where('email', '==', data['email']).stream()
        user = {}    
        for us in users:
            user = us.to_dict()
        if user:
            flash('Email has been registered', 'danger')
            return redirect(url_for('register'))

        data['password'] = generate_password_hash(request.form['password'], 'sha256')
        # kita masukkan datanya ke database
        db.collection('users').document().set(data)

        send_wa(f"Halo {data['name']} selamat siang. Email kamu: {data['email']}. password kamu: {data['password']}", data["number"])
        
        flash('Berhasil Register', 'success')

        # redirect ke halaman login
        return redirect(url_for('index'))

    # menampilkan halaman register
    return render_template('register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    # menentukan method
    if request.method == "POST":

        # ambil data dari form
        data = {
            "email": request.form["email"],
            "password": request.form["password"]
        }
        # lakukan pengecekan
        users = db.collection('users').where("email", "==", data["email"]).stream()
        user = {}

        for us in users:
            user = us.to_dict()

        if user:
            if check_password_hash(user["password"], data["password"]):
                session["user"] = user
                flash('selamat anda berhasil login', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('maaf password anda salah', 'danger')
                return redirect(url_for('login'))
        else:
            flash('email belum terdaftar', 'danger')
            return redirect(url_for('login'))

# pake penggunaan string

    if 'user' in session:
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))




if __name__ == "__main__":
    app.run(debug=True)