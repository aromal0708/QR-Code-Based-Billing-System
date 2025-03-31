from flask import Blueprint, session, redirect

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/process_payment', methods=['POST'])
def process_payment():
    session.pop('cart', None)  # Clear the cart after payment
    return "Payment Successful!"
