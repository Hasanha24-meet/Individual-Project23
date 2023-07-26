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
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"first_name": first_name, "email": email, "password": password, "last_name": last_name}
            db.child("Users").child(UID).set(user)
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            print(e)
            flash("Signup Failed. Please try again.", "error")
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            user_id = login_session['user']['localId']
            user_data = db.child("Users").child(user_id).get().val()
            login_session['user_data'] = user_data
            return redirect(url_for('home'))
        except:
            flash("Authentication Failed. Please check your credentials.", "error")
    return render_template("login.html")


@app.route('/logout')
def logout():
    login_session.clear()
    return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user' not in login_session:
        return redirect(url_for('login'))

    user_id = login_session['user']['localId']

    if request.method == 'POST':
        if request.form['submit'] == 'add':
            try:
                name = request.form['name']
                db.child("Users").child(user_id).child("items").push(name)
                user_data = db.child("Users").child(user_id).get()
                to = user_data.val() if user_data else []
                return render_template('home.html', t=to.values())
            except:
                flash("Error adding item. Please try again.", "error")
        elif request.form['submit'] == 'delete':
            db.child("Users").child(user_id).child("items").remove()
            login_session['user_data'] = db.child("Users").child(user_id).get().val()
            flash("All items deleted.", "success")
        return render_template('home.html')

    user_data = db.child("Users").child(user_id).get()
    to = user_data.val() if user_data else []
    return render_template('home.html', t=to.values())


if __name__ == '__main__':
    app.run(debug=True)