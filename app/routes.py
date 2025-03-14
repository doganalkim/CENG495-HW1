from flask import Blueprint, jsonify, request, render_template, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from bson.objectid import ObjectId
from .db import get_db
import base64

bp = Blueprint('main', __name__)

auth  = Blueprint('auth', __name__)

db = get_db()
user_collection = db.users
item_collection = db.items

@bp.route('/')
def index():

    all_items = item_collection.find()

    return render_template('list.html', items = all_items )

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

            return redirect(url_for('main.index'))

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
    all_items = item_collection.find()

    return render_template('admin_panel.html', users = all_users, items = all_items)

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

@bp.route('/delete-items', methods=["POST"])
def delete_items():
    if request.method != 'POST':
        return render_template('admin_panel.html')

    selected_items = request.form.getlist('item_id')

    selected_ids = [ObjectId(id) for id in selected_items]

    result = item_collection.delete_many({'_id':{'$in': selected_ids}})

    print(f'{result} items have been deleted!')

    return redirect(url_for('main.admin_panel'))

@bp.route('/add-item', methods = ['POST'])
def add_item():
    if request.method != 'POST':
        return render_template('admin_panel.html')

    item_name = request.form.get('item_name')
    item_price = request.form.get('item_price')
    item_description = request.form.get('description')
    item_seller = request.form.get('seller_name')
    item_photo = request.files.get('item_photo')
    item_photo_b64 = base64.b64encode(item_photo.read()).decode('utf-8')
    item_type = request.form.get('item_type')

    # <option>Vinyls</option>
    # <option>Antique Furniture</option>
    # <option>GPS Sport Watches</option>
    # <option>Running Shoes</option>

    # print(f'{item_name}')
    # print(f'{item_description}')
    # print(f'{item_seller}')
    # print(f'{item_photo_b64}')
    # print(f'{item_type}')

    if item_name == None or item_price == None or item_description == None or item_seller == None or item_photo_b64 == None or item_type == None:
        print(f'None Detected!')
        return render_template('admin_panel.html')

    if item_type == 'Vinyls':
        age = request.form.get('age')

        item_collection.insert_one(
            {"name":item_name,
            "price": item_price,
            "description":item_description,
            "seller":item_seller,
            "photo":item_photo_b64,
            "type": item_type,
            "age": age
        })

        print(f'inserted Vinyls')

    elif item_type == 'Antique Furniture':
        age = request.form.get('age')
        material = request.form.get('material')

        item_collection.insert_one(
            {"name":item_name,
            "price": item_price,
            "description":item_description,
            "seller":item_seller,
            "photo":item_photo_b64,
            "type": item_type,
            "age": age,
            "material": material,
        })
    elif item_type == 'GPS Sport Watches':
        battery_life = request.form.get('battery_life')

        item_collection.insert_one(
            {"name":item_name,
            "price": item_price,
            "description":item_description,
            "seller":item_seller,
            "photo":item_photo_b64,
            "type": item_type,
            "battery": battery_life
        })
    elif item_type == 'Running Shoes':
        size = request.form.get('size')
        material = request.form.get('material')

        item_collection.insert_one(
            {"name":item_name,
            "price": item_price,
            "description":item_description,
            "seller":item_seller,
            "photo":item_photo_b64,
            "type": item_type,
            "size": size,
            "material": material
        })
    #print(f'item_received: {item_name} {item_photo_b64}')

    return redirect(url_for('main.admin_panel'))
    
@bp.route('/item-detail', methods = ['GET'])
def item_detail():
    if request.method != 'GET':
        return redirect(url_for('main.index'))
    
    item_id = request.args.get('item_id')

    print(f'Request for {item_id}')

    return redirect(url_for('main.index'))
    
