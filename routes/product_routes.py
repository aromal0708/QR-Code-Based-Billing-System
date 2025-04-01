from flask import Blueprint, request, redirect, url_for, flash, render_template
from database import get_db_connection
import qrcode;
import os

product_bp = Blueprint('product', __name__)
QR_CODE_DIR = os.path.join(os.getcwd(), 'qr_code')
os.makedirs(QR_CODE_DIR, exist_ok=True)

@product_bp.route('/')
def home():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    db.close()
    return render_template('index.html', products=products)

@product_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form.get('product_id')  # User must provide this
        product_name = request.form.get('product_name')
        price = request.form.get('price')

        if not product_id or not product_name or not price:
            flash('Product ID, name, and price are required!', 'danger')
            return redirect(url_for('product.add_product'))

        try:
            db = get_db_connection()
            cursor = db.cursor()

            # Insert product into database
            cursor.execute("INSERT INTO products (product_id, product_name, price) VALUES (%s, %s, %s)", 
                           (product_id, product_name, price))
            db.commit()

            # Generate and save QR code
            generate_qr_code(product_id)

            flash('Product added successfully!', 'success')
            return redirect(url_for('product.add_product'))
        except Exception as e:
            flash(f"Error: {str(e)}", 'danger')
        finally:
            db.close()

    return render_template('add_product.html')

# Function to generate QR code for a product
def generate_qr_code(product_id):
    qr_data = f"Product ID: {product_id}"
    qr = qrcode.make(qr_data)
    qr_path = os.path.join(QR_CODE_DIR, f"{product_id}.png")
    qr.save(qr_path)