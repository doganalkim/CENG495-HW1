from flask import Blueprint, jsonify, request, render_template, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from bson.objectid import ObjectId
from .db import get_db
import base64
from datetime import datetime
import urllib.parse

bp = Blueprint('main', __name__)

auth  = Blueprint('auth', __name__)

db = get_db()
user_collection = db.users
item_collection = db.items
rate_collection = db.rates
review_collection = db.reviews

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
            session['user_id'] = str(user_data['_id'])
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
    session.pop('user_id', None)
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

    #print(f'{result} users have been deleted!')

    rate_collection.delete_many({'user_id': {'$in': selected_users} })
    review_collection.delete_many({'user_id': {'$in': selected_users}})

    return redirect(url_for('main.admin_panel'))

@bp.route('/delete-items', methods=["POST"])
def delete_items():
    if request.method != 'POST':
        return render_template('admin_panel.html')

    selected_items = request.form.getlist('item_id')

    selected_ids = [ObjectId(id) for id in selected_items]

    result = item_collection.delete_many({'_id':{'$in': selected_ids}})

    print(f'{result} items have been deleted!')

    rate_collection.delete_many({'item_id': {'$in': selected_items} })
    review_collection.delete_many({'item_id': {'$in': selected_items}})

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
    if request.method != 'GET' or 'username' not in session:
        return redirect(url_for('main.index'))
    
    item_id = request.args.get('item_id')

    avg_rating = 0
    aggregate_input = [
        {"$match":{"item_id": item_id}},
        {"$group": 
            {
                "_id":"$item_id",
                "average_rating": {"$avg": "$rate"}
            }
        }
    ]

    avg_rating_cursor = rate_collection.aggregate(aggregate_input)

    for rate in avg_rating_cursor:
        avg_rating = rate.get('average_rating',0)

    #print(f'AVG RATING: {avg_rating}')

    avg_rating_percent = avg_rating * 10

    detailed_item = item_collection.find_one({'_id': ObjectId(item_id)})

    reviews = review_collection.find({'item_id':item_id})

    return render_template('item_details.html', item = detailed_item, rating = avg_rating, rating_percent = avg_rating_percent, reviews = reviews)
    
@bp.route('/rate/<id>', methods = ['POST'])
def rate_item(id):
    if request.method != 'POST' or 'username' not in session:
        return redirect(url_for('main.index'))

    item_rate = int(request.form['rate'])
    user_id = session.get('user_id')

    previous_rate = rate_collection.find_one( {'user_id':user_id, 'item_id': id})

    print(f'request for {id}')
    print(f'Rate: {item_rate}')

    if previous_rate:
        rate_collection.update_one({'user_id': user_id, 'item_id':id }, {'$set':{'rate':item_rate }})
    else:
        rate_collection.insert_one({'user_id': user_id, 'item_id':id, 'rate': item_rate })

    return redirect(url_for('main.index'))

@bp.route('/review/<id>', methods = ['POST'])
def review(id):
    if request.method != 'POST' or 'username' not in session:
        return redirect(url_for('main.index'))

    review = request.form.get('review')
    user_id = session.get('user_id')
    username = session.get('username')
    current_date = datetime.now()

    previous_review = rate_collection.find_one({'user_id':user_id, 'item_id':id})

    if previous_review:
        review_collection.update_one({'user_id': user_id, 'item_id': id,  'username': username }, {'$set':{'review':review, 'date':current_date}})
    else:
        review_collection.insert_one({'user_id': user_id, 'item_id': id, 'review':review, 'date': current_date, 'username': username })

    print(f'Comment: {review} for id: {id}')
    return redirect(url_for('main.index'))

@bp.route('/profile', methods = ['GET'])
def profile():
    if request.method != 'GET' or 'username' not in session:
        return redirect(url_for('main.index'))

    username = session.get('username')
    user_id = session.get('user_id')
    avg_rating = 0

    aggregate_input = [
        {"$match":{"user_id": user_id}},
        {"$group": 
            {
                "_id":"$user_id",
                "average_rating": {"$avg": "$rate"}
            }
        }
    ]

    avg_rating_cursor = rate_collection.aggregate(aggregate_input)

    for rate in avg_rating_cursor:
        avg_rating = rate.get('average_rating',0)

    #print(f'AVG RATING: {avg_rating}')

    my_reviews = review_collection.find({'user_id':user_id})
    
    return render_template('profile.html', username = username, rating = avg_rating, reviews = my_reviews)

@bp.route("/categorize/<item_category>", methods = ['GET'])
def categorize(item_category):
    if request.method != 'GET':
        return redirect(url_for('main.index'))

    item_category =  urllib.parse.unquote(item_category)

    items = item_collection.find({'type': item_category})

    print(f'category:{item_category}')

    return render_template('list.html', items = items)

@bp.route("/search", methods = ['GET'])
def search():
    if request.method != 'GET':
        return redirect(url_for('main.index'))
    
    query = request.args.get('query')
    items = item_collection.find({'name': {'$regex':query, "$options": "i" }})

    return render_template('list.html', items = items)
