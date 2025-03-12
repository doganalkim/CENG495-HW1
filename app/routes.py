from flask import Blueprint, jsonify, request, render_template, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from bson.objectid import ObjectId
from .db import get_db

bp = Blueprint('main', __name__)

auth  = Blueprint('auth', __name__)

db = get_db()
user_collection = db.users
item_collection = db.items

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        if username is None or password is None:

            error = "Provide credentials"

            flash(error)

        user_data = user_collection.find_one({"username":username})

        if user_data is not None and check_password_hash(user_data['password'], password):

            session['username'] = username
            session['admin'] = False

            if user_data.get('admin'):
                session['admin'] = True

            return render_template('index.html')

        else:
            print("check failed")
            error = 'Invalid username or password'
        
        flash(error)
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    session.pop('admin', None)
    session.pop('username', None)
    return redirect(url_for('main.index'))


@bp.route('/admin-panel')
def admin_panel():
    is_admin = session.get('admin') 
    if is_admin != True:
        return  redirect(url_for('main.index'))

    all_users = user_collection.find()
    return render_template('admin_panel.html', users = all_users)

@bp.route('/register', methods = ['POST'])
def register():
    if request.method != 'POST':
        return render_template('admin_panel.html')

    username = request.form['username']
    password = request.form['password']
    avg_rating = 0
    reviews = 0

    hashed_password = generate_password_hash(password)

    user_collection.insert_one({"username":username, "password":hashed_password, "avgRating":avg_rating, "reviews": reviews })

    return redirect(url_for('main.admin_panel'))

@bp.route('/delete-users', methods = ['POST'])
def delete_users():
    if request.method != 'POST':
        return render_template('admin_panel.html')
    
    selected_users = request.form.getlist('user_id')

    selected_ids = [ObjectId(id) for id in selected_users]

    result = user_collection.delete_many({'_id':{'$in': selected_ids }})

    print(f'{result} users have been deleted!')


    return redirect(url_for('main.admin_panel'))


    