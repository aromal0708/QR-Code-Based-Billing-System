import os
import qrcode
from database import get_db_connection

# Ensure the qr_code directory exists
QR_CODE_DIR = "qr_code"
os.makedirs(QR_CODE_DIR, exist_ok=True)

def generate_qr_code(product_id, product_name):
    """Generate a QR code for a product and save it as an image."""
    qr_data = f"Product ID: {product_id}, Name: {product_name}"
    qr = qrcode.make(qr_data)
    qr_path = os.path.join(QR_CODE_DIR, f"{product_id}.png")
    qr.save(qr_path)
    print(f"QR Code saved: {qr_path}")

def generate_qr_codes_for_all_products():
    """Generate QR codes for all products in the database."""
    db = get_db_connection()
    cursor = db.cursor()
    
    cursor.execute("SELECT product_id, product_name FROM products")
    products = cursor.fetchall()
    
    for product in products:
        product_id, product_name = product
        qr_path = os.path.join(QR_CODE_DIR, f"{product_id}.png")

        # Generate QR code only if it doesn't already exist
        if not os.path.exists(qr_path):
            generate_qr_code(product_id, product_name)
    
    db.close()

def add_product(product_name, price):
    """Add a new product to the database and generate its QR code."""
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("INSERT INTO products (product_name, price) VALUES (%s, %s)", (product_name, price))
    db.commit()

    # Fetch the last inserted product ID
    cursor.execute("SELECT LAST_INSERT_ID()")
    product_id = cursor.fetchone()[0]

    # Generate QR code for the new product
    generate_qr_code(product_id, product_name)

    db.close()
    print(f"Product '{product_name}' added with ID {product_id} and QR Code generated.")

# Generate QR codes for existing products
generate_qr_codes_for_all_products()
