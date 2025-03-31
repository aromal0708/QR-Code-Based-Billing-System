from flask import Flask, render_template, request, redirect, session  
import MySQLdb  
app = Flask(__name__)  
app.secret_key = 'secret123'  

# MySQL Config  
db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="qr")  
cursor = db.cursor()

# Home Page  
@app.route('/')  
def home():  
    return render_template('index.html')

# Add to Cart  
@app.route('/add_to_cart', methods=['POST'])  
def add_to_cart():  
    product_id = request.form['product_id']  
    cursor.execute("SELECT * FROM products WHERE id=%s", (product_id,))  
    product = cursor.fetchone()  

    if product:  
        if 'cart' not in session:  
            session['cart'] = []  
        session['cart'].append({'id': product[0], 'name': product[1], 'price': product[2]})  

    return redirect('/cart')

# View Cart  
@app.route('/cart')  
def view_cart():  
    cart = session.get('cart', [])  
    total_price = sum(item['price'] for item in cart)  
    return render_template('cart.html', cart=cart, total_price=total_price)

# Checkout Page  
@app.route('/checkout')  
def checkout():  
    total_price = sum(item['price'] for item in session.get('cart', []))  
    return render_template('checkout.html', total_price=total_price)

# Remove from Cart  
@app.route('/remove_from_cart', methods=['POST'])  
def remove_from_cart():  
    product_id = int(request.form['product_id'])  
    session['cart'] = [item for item in session['cart'] if item['id'] != product_id]  
    return redirect('/cart')

# Process Payment  
@app.route('/process_payment', methods=['POST'])  
def process_payment():  
    return "Payment Successful!"

if __name__ == '__main__':  
    app.run(debug=True)
