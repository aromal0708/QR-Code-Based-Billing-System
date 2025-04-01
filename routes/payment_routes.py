from flask import Blueprint, request, session, redirect, url_for, flash
import uuid
from database import get_db_connection  # Importing database connection

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/process_payment', methods=['POST'])
def process_payment():
    if 'session_id' not in session:
        return redirect(url_for('cart.checkout'))  # Redirect to checkout if no session

    db = get_db_connection()
    cursor = db.cursor()

    # Get the total price from the session cart data
    cart = session.get('cart', [])
    total_price = sum(item['total_price'] for item in cart)  # Calculate the total from the cart session

    # Generate a unique transaction ID
    transaction_id = str(uuid.uuid4())

    # Insert into transactions table
    cursor.execute("INSERT INTO transactions (TransactionID, user_id, product_id, product_name, quantity, total_price) VALUES (%s, %s, %s, %s, %s, %s)", 
                   (transaction_id, None, None, None, None, total_price))  # 'None' can be used for products and user_id since you're not saving item-level details
    db.commit()

    # Clear the session after storing the transaction
    session.clear()

    # Flash success message
    flash("Payment successful! Your transaction has been recorded.", "success")

    return redirect(url_for('product.home'))  # Redirect to home page  
