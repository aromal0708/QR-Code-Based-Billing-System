from flask import Blueprint, session, request, redirect, render_template
from database import get_db_connection

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total_price = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE id=%s", (product_id,))
    product = cursor.fetchone()
    db.close()

    if product:
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append({'id': product[0], 'name': product[1], 'price': product[2]})

    return redirect('/cart')

@cart_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = int(request.form['product_id'])
    session['cart'] = [item for item in session['cart'] if item['id'] != product_id]
    return redirect('/cart')
