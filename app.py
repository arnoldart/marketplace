# app.py
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from utils.db_utils import get_products, get_product_by_id, add_cart, verify_user, user_exists, create_user, get_user_cart, remove_item_from_cart, clear_user_cart
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_id = verify_user(username, password)

        if user_id:
            session['user_id'] = user_id
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not user_exists(username):
            create_user(username, password)
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose another username.', 'error')

    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    flash('Logout successful!', 'success')
    return redirect(url_for('home'))

@app.route('/')
def home():
    if 'username' in session:
        products = get_products()
        return render_template('index.html', products=products)
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

@app.route('/detail/<int:product_id>')
def detail(product_id):
    if 'username' in session:
        products = get_products()
        productId = get_product_by_id(product_id)

        return render_template('detail.html', productId=productId, products=products)
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

@app.route('/cart')
def cart():
    if 'username' in session:
        user_id = session.get('user_id')

        cart_data = get_user_cart(user_id)
        
        return render_template('cart.html', cart_data=cart_data)
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' in session:
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))
        user_id = int(request.form.get('user_id'))
        
        add_cart(user_id, product_id, quantity)

        return redirect(url_for('detail', product_id=product_id))
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/remove_from_cart/<int:cart_item_id>')
def remove_from_cart(cart_item_id):
    if 'user_id' in session:
        remove_item_from_cart(cart_item_id)
        flash('Item removed from cart.', 'success')
        return redirect(url_for('cart'))
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    
    
@app.route('/checkout')
def checkout():
    if 'user_id' in session:
        user_id = session['user_id']
        cart_data = get_user_cart(user_id)

        total = calculate_cart_total(cart_data)

        return render_template('checkout.html', cart_data=cart_data, total=total)
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

def calculate_cart_total(cart_data):
    total = 0
    for item in cart_data:
        total += item['price'] * item['quantity']
    return total

@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' in session:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')

        user_id = session.get('user_id')
        cart_data = get_user_cart(user_id)
        total = calculate_cart_total(cart_data)

        return render_template('order_receipt.html', 
                            first_name=first_name, 
                            last_name=last_name,
                            email=email,
                            phone=phone,
                            address=address,
                            total=total,
                            cart_data=get_user_cart(user_id)
                            ) 
    else:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    

@app.route('/clear_cart')
def clear_cart():
    user_id = session.get('user_id')
    clear_user_cart(user_id)
    return redirect(url_for('home'))