from flask import Blueprint, session, request, redirect, render_template, jsonify, flash
from database import get_db_connection
import uuid  # Import UUID for unique TransactionID

cart_bp = Blueprint('cart', __name__)

# View Cart Route
@cart_bp.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total_price = sum(item['total_price'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

# Add to Cart Route (Fixing KeyError and Price Calculation)
@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    if not product_id:
        return jsonify({'error': 'Product ID is missing'}), 400

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT product_id, product_name, price FROM products WHERE product_id=%s", (product_id,))
    product = cursor.fetchone()
    db.close()

    if not product:
        return jsonify({'error': 'Product not found in database'}), 404

    cart = session.get('cart', [])
    found = False

    for item in cart:
        if item['id'] == product[0]:
            item['quantity'] += 1
            unit_price = item.get('unit_price', item['price'])  # Ensure unit price exists
            item['total_price'] = round(unit_price * item['quantity'], 2)
            found = True
            break

    if not found:
        unit_price = round(float(product[2]), 2)
        cart.append({
            'id': product[0],
            'name': product[1],
            'unit_price': unit_price,  # Store unit price separately
            'price': unit_price,  # Keep 'price' for backward compatibility
            'quantity': 1,
            'total_price': unit_price
        })

    session['cart'] = cart
    session.modified = True
    return jsonify({'message': 'Product added to cart', 'cart_count': len(session['cart'])})

# Remove from Cart Route (Fix KeyError for 'unit_price')
@cart_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = int(request.form.get('product_id'))
    cart = session.get('cart', [])

    for item in cart:
        if item['id'] == product_id:
            if item['quantity'] > 1:
                item['quantity'] -= 1
                unit_price = item.get('unit_price', item['price'])  # Handle missing unit_price
                item['total_price'] = round(unit_price * item['quantity'], 2)
            else:
                cart.remove(item)
            break

    session['cart'] = cart
    session.modified = True
    return redirect('/cart')

# Checkout Route (Ensure correct total amount)
@cart_bp.route('/checkout', methods=['GET'])
def checkout():
    # Ensure session ID exists
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())  # Generate a new session if not exists

    return render_template('checkout.html')

@cart_bp.route('/cancel_purchase', methods=['POST'])
def cancel_purchase():
    session.pop('cart', None)
    session.clear()
    flash("Purchase cancelled. Cart is now empty.", "info")
    return redirect('/cart')
    