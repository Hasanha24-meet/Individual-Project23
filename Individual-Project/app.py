from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
config = {
    "apiKey": "AIzaSyAtMFJ2aTTUym4SRWI88Zop6sv1mNMXAlM",
    "authDomain": "personal-project-30557.firebaseapp.com",
    "databaseURL": "https://personal-project-30557-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "personal-project-30557",
    "storageBucket": "personal-project-30557.appspot.com",
    "messagingSenderId": "25479274186",
    "appId": "1:25479274186:web:eeabed54c90e80b3829e33",
    "measurementId": "G-1JFXNZXDJV",
    "databaseURL": "https://personal-project-30557-default-rtdb.europe-west1.firebasedatabase.app/"
}

#Code goes below here
@app.route('/', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        password = request.form['password']
        last_name = request.form['last_name']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"first_name": first_name, "email": email, "password": password, "last_name": last_name}
            db.child("Users").child(UID).set(user)
            return redirect(url('home'))
        except:
            error = "Signup Failed"
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():  
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url('login.html'))
        except:
            error = "Authentication Failed"
    return render_template("/login")

#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)