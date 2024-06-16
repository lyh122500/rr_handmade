from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Category, Product, Cart, CartItem, User
from flask import current_app as app


@app.route('/')
def home():
    categories = Category.objects.all()
    return render_template('index.html', categories=categories)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password = request.form.get('password')
        user = User(email=email, first_name=first_name, password=generate_password_hash(password))
        user.save()
        flash('Registration successful, please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.objects(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = str(user.id)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/category/<category_id>')
def category(category_id):
    category = Category.objects.get_or_404(id=category_id)
    products = Product.objects(category=category)
    return render_template('category.html', category=category, products=products)


@app.route('/product/<product_id>')
def product(product_id):
    product = Product.objects.get_or_404(id=product_id)
    return render_template('product.html', product=product)


@app.route('/add_to_cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.objects.get_or_404(id=product_id)
    quantity = int(request.form.get('quantity', 1))

    if 'user_id' not in session:
        flash('Please login to add items to your cart.', 'warning')
        return redirect(url_for('login'))

    user = User.objects.get(id=session['user_id'])

    cart = Cart.objects(user=user).first()
    if not cart:
        cart = Cart(user=user)

    for item in cart.items:
        if item.product == product:
            item.quantity += quantity
            break
    else:
        cart.items.append(CartItem(product=product, quantity=quantity))

    cart.save()
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    if 'user_id' not in session:
        flash('Please login to view your cart.', 'warning')
        return redirect(url_for('login'))

    user = User.objects.get(id=session['user_id'])
    cart = Cart.objects(user=user).first()
    if not cart:
        cart = Cart(items=[])

    return render_template('cart.html', cart=cart)


@app.route('/remove_from_cart/<product_id>', methods=['POST'])
def remove_from_cart(product_id):
    user = User.objects.get(id=session['user_id'])
    cart = Cart.objects(user=user).first()
    cart.items = [item for item in cart.items if str(item.product.id) != product_id]
    cart.save()
    return redirect(url_for('cart'))
