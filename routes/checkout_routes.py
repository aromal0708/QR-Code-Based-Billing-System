from flask import Blueprint, session, render_template, flash, redirect
import uuid
from database import get_db_connection  # Ensure this function exists for DB connection

# Create a Blueprint for checkout
checkout_bp = Blueprint("checkout", __name__)


@checkout_bp.route("/checkout")
def checkout():
    cart = session.get("cart", [])

    if not cart:
        flash("Cart is empty!", "error")
        return redirect("/cart")

    total_price = sum(
        item["total_price"] for item in cart
    )  # Ensure total_price is calculated correctly
    return render_template("checkout.html", total_price=total_price)

@checkout_bp.route("/process_payment", methods=["POST"])
def process_payment():
    cart = session.get("cart", [])
    if not cart:
        flash("Cart is empty!", "error")
        return redirect("/cart")

    db = get_db_connection()
    cursor = db.cursor()

    user_id = session.get("user_id", None)  # Ensure user_id exists
    transaction_id = str(uuid.uuid4())[:20]  # Generate unique TransactionID

    try:
        for item in cart:
            cursor.execute(
                """
    INSERT INTO transactions (TransactionID, user_id, product_id, product_name, quantity, total_price)
    VALUES (%s, %s, %s, %s, %s, %s)
""",
                (
                    transaction_id,
                    user_id,
                    item["id"],
                    item["name"],
                    item["quantity"],
                    item["total_price"],
                ),
            )

        db.commit()  # Commit transaction after inserting all cart items
        flash("Payment Successful!", "success")
        session.pop("cart", None)  # Clear cart after successful checkout

    except Exception as e:
        db.rollback()  # Rollback in case of an error
        flash("An error occurred during checkout!", "error")
        print(f"Checkout Error: {e}")  # Debugging statement

    db.close()
    return redirect("/cart")
