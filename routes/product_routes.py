from flask import Blueprint, render_template
from database import get_db_connection

product_bp = Blueprint('product', __name__)

@product_bp.route('/')
def home():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    db.close()
    return render_template('index.html', products=products)
