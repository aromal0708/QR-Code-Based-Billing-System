from flask import Blueprint, session, request, redirect, render_template, jsonify, flash, url_for
from database import get_db_connection
import uuid  # Import UUID for unique TransactionID

cart_bp = Blueprint('cart', __name__)

# View Cart Route
@cart_bp.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    # Safely calculate total price with error handling
    total_price = 0
    for item in cart:
        try:
            total_price += float(item.get('total_price', 0))
        except (ValueError, TypeError):
            continue
    total_price = round(total_price, 2)
    return render_template('cart.html', cart=cart, total_price=total_price)

# Add to Cart Route
@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    if not product_id:
        return jsonify({'error': 'Product ID is missing'}), 400

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT product_id, product_name, price FROM products WHERE product_id=%s", (product_id,))
        product = cursor.fetchone()
        db.close()

        if not product:
            return jsonify({'error': 'Product not found in database'}), 404

        # Safely convert price to float
        try:
            unit_price = round(float(product[2]), 2)
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid product price'}), 400

        cart = session.get('cart', [])
        found = False

        for item in cart:
            if item['id'] == product[0]:
                item['quantity'] += 1
                unit_price = item.get('unit_price', item.get('price', 0))
                item['total_price'] = round(unit_price * item['quantity'], 2)
                found = True
                break

        if not found:
            cart.append({
                'id': product[0],
                'name': product[1],
                'unit_price': unit_price,
                'price': unit_price,
                'quantity': 1,
                'total_price': unit_price
            })

        session['cart'] = cart
        session.modified = True
        return jsonify({'message': 'Product added to cart', 'cart_count': len(session['cart'])})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Remove from Cart Route
@cart_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    try:
        product_id = int(request.form.get('product_id'))
    except (ValueError, TypeError):
        flash("Invalid product ID", "error")
        return redirect('/cart')

    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            if item['quantity'] > 1:
                item['quantity'] -= 1
                unit_price = item.get('unit_price', item.get('price', 0))
                item['total_price'] = round(unit_price * item['quantity'], 2)
            else:
                cart.remove(item)
            break

    session['cart'] = cart
    session.modified = True
    return redirect('/cart')

# Checkout Route
@cart_bp.route('/checkout')
def checkout():
    if 'cart' not in session or not session['cart']:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('cart.view_cart'))

    # Safely calculate total price
    total_price = 0
    for item in session['cart']:
        try:
            total_price += float(item.get('total_price', 0))
        except (ValueError, TypeError):
            continue
    total_price = round(total_price, 2)

    return render_template("checkout.html", total_price=total_price)

@cart_bp.route('/cancel_purchase', methods=['POST'])
def cancel_purchase():
    session.pop('cart', None)
    session.clear()
    flash("Purchase cancelled. Cart is now empty.", "info")
    return redirect('/cart')
    