from flask_app import app
from flask import render_template, redirect, request, session, flash

from flask_app.models.user import User
from flask_app.models.recipe import Recipe

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("login_and_register.html")


@app.route("/register", methods=["POST"])
def register():
    print('form = ', request.form)
    if not User.validate_user(request.form):
        return redirect("/")
    user_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(user_data)
    session['user_id'] = id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    recipes = Recipe.get_recipes_by_user_id(data)
    return render_template(
        "dashboard.html",
        user=User.get_by_id(data),
        recipes=recipes,
    )


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email/Password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/logout')
def logout():

    session.clear()
    return redirect('/')
