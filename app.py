from flask import Flask
from database import get_db_connection
from routes.cart_routes import cart_bp
from routes.product_routes import product_bp
from routes.checkout_routes import checkout_bp
from routes.payment_routes import payment_bp

app = Flask(__name__)
app.secret_key = 'secret123'

app.register_blueprint(cart_bp)
app.register_blueprint(product_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(checkout_bp)

if __name__ == '__main__':
    app.run(debug=True)
