from flask import Blueprint, session, request, redirect, url_for, flash
from database import get_db_connection
import uuid

payment_bp = Blueprint('payment', __name__)

import uuid

@payment_bp.route('/process_payment', methods=['POST'])
def process_payment():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())  # Generate a unique session ID if not exists

    db = get_db_connection()
    cursor = db.cursor()

    transaction_id = session['session_id']  # Use session ID as transaction ID
    cart = session.get('cart', [])

    if not cart:
        flash("Your cart is empty. Please add items before making a payment.", "warning")
        return redirect(url_for('cart.checkout'))  # Redirect to checkout

    total_price = sum(item['total_price'] for item in cart)

    try:
        # Store only transaction ID and total price in DB
        cursor.execute(
            "INSERT INTO transactions (TransactionID, total_price) VALUES (%s, %s)",
            (transaction_id, total_price)
        )
        db.commit()
        
        flash("✅ Payment successful! Your transaction has been recorded.", "success")

    except Exception as e:
        db.rollback()  # Rollback in case of an error
        flash(f"❌ Payment failed: {str(e)}", "danger")

    finally:
        cursor.close()
        db.close()

    # Clear session after successful payment
    session.clear()

    return redirect(url_for('product.home'))  # Redirect to home page