from flask import Flask, render_template, jsonify, request, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import load_users_from_db, load_users_from_username, engine, load_users_from_email, insert_user, get_user_id, insert_movies, get_movies, get_monthly_movies
import os
import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

year_now = datetime.date.today().year
month_now = datetime.date.today().month
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
dict_months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

@app.route('/')
def hello():
    if 'loggedin' in session:
        try:
            movies = get_monthly_movies(session['id'], month_now)
            print(movies)
        except:
            movies = []
            flash('Something went wrong, please refresh the page', category='error')
    else:
        return render_template('home.html', movies=[])
    return render_template('home.html', session=session, movies=movies)

@app.route('/animation')
def animation():
    return render_template('animation.html', session=session)

@app.route('/lista')
def lista():
    if 'loggedin' in session:
        try:
            movies = get_movies(session['id'])
        except:
            movies = []
            flash('Something went wrong, please refresh the page', category='error')
    else:
        return render_template('lista.html', movies=[], months=months)
    return render_template('lista.html', movies=movies, months=months, now=year_now, dict_months=dict_months)

@app.route("/users/<name>")
def show_user_profile(name):
    user = load_users_from_username(name)
    return jsonify(user)

@app.route('/data')
def list_about():
    if 'loggedin' in session:
        users = get_user_id(session['id'])
        movies = get_movies(session['id'])
    return jsonify(movies)


@app.route('/register', methods=['GET', 'POST'])
def register():
        """Register user"""
        if request.method == "POST":
            # Require username
            email = request.form.get("email")
            name = request.form.get("username")
            password = request.form.get("password")

            # Check if email already exists
            users = load_users_from_email(email)
            usernames = load_users_from_username(name)
            if users:
                flash('Email already exists', category='error')
            elif not email or len(email) < 4:
                flash('Email must be valid', category='error')
            if usernames:
                flash('Username already taken', category='error')
            elif len(name) < 2 :
                flash('Username must be greater than 1 character', category='error')
            # Check and validate passwords
            elif not password:
                flash("Must provide password", category='error')
            elif len(password) < 3:
                flash("Password must be greater than 3 characters", category='error')
            else:
            # Create hash of password to insert into the database
                hash = generate_password_hash(request.form.get("password"), method='sha256')

                insert_user(name, email, password=hash)
                flash('Account created', category='success')

                return redirect("/")

        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            users = load_users_from_email(email)
        except:
            users = []
            flash('Something went wrong, please try again', category='error')
        if users != []:
            if users[0]['email'] == email and users[0]['password'] == password:
                session['loggedin'] = True
                session['id'] = users[0]['id']
                session['email'] = users[0]['email']
                flash ('Logged in successfully!', category='success')
                return redirect('/')
            # If account exists in accounts table in out database
            else:
            # Account doesnt exist or username/password incorrect
                flash ('Incorrect username/password!', category='error')
        else:
            flash ('Something went wrong, please try again', category='error')
    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html", session=session)

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        users = get_user_id(session['id'])
        try:
            movies = get_movies(session['id'])
            length = len(movies)
            lenght_month = len(get_monthly_movies(session['id'], month_now))
            rating = 0
            genres = {}
            for movie in movies:
                rating += movie['rating']
                genres[movie['genre']] = genres.get(movie['genre'], 0) + 1
                favorite_genre = max(genres, key=genres.get)
        except:
            movies = []
            flash('Something went wrong, please refresh the page', category='error')
        return render_template('profile.html', user=users[0], movies=movies, length = length, lmonth=lenght_month, avg_rating=round(rating/length, 2), favorite_genre=favorite_genre)
    return redirect('/login')

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    # Redirect to login page
    return redirect('/')

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == "POST":
        try:
            if 'loggedin' in session:
                parent_id = get_user_id(session['id'])
                title = request.form["title"]
                director = request.form["director"]
                year = request.form["year"]
                date = request.form["date"]
                genre = request.form["genre"]
                rating = request.form["rating"]
                rewatch = request.form["rewatch"] # 0 false, 1 true
                tv = request.form["tv"]
                print(title, director, year, date, genre, rating, rewatch, tv, session['id'])
                insert_movies(title, director, genre, year, date, rating, rewatch, tv, session['id'])
                flash('Movie added', category='success')
            else:
                flash('You need to be logged in to add a movie', category='error')
        except:
            redirect('/add_movie')
            flash('Something went wrong, please try again', category='error')
            
    return render_template('add_movie.html')
        

if __name__ == '__main__':
    app.run(debug=True)