# QR Code-Based Billing System

A modern billing system that leverages QR codes for quick and efficient product scanning and checkout. This project allows users to scan product QR codes, add items to cart, and complete the purchase seamlessly.

## Features

- **QR Code Scanning**: Scan product QR codes to automatically add them to cart
- **Shopping Cart Management**: Add, remove, and update products in your cart
- **Responsive UI**: Modern and user-friendly interface that works on various devices
- **Secure Checkout**: Complete the purchase with multiple payment options
- **Transaction History**: View past transactions and order details

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Database**: MySQL
- **QR Code Processing**: jsQR library

## Project Structure

```
.
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── database.py             # Database connection management
├── db.queries.txt          # Database setup queries
├── generate_qr.py          # QR code generation utility
├── requirements.txt        # Python dependencies
├── routes/                 # Route handlers
│   ├── cart_routes.py      # Cart-related endpoints
│   ├── checkout_routes.py  # Checkout process endpoints
│   ├── payment_routes.py   # Payment processing endpoints
│   └── product_routes.py   # Product-related endpoints
├── static/                 # Static assets (CSS, JS, images)
└── templates/              # HTML templates
    ├── add_product.html    # Add product form
    ├── cart.html           # Shopping cart page
    ├── checkout.html       # Checkout page
    └── index.html          # Home page with QR scanner
```

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- MySQL Server installed and running
- Git (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/qr-code-billing-system.git
cd qr-code-billing-system
```

### Step 2: Create a Virtual Environment and Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Set Up the Database

1. Make sure your MySQL server is running
2. Update the database configuration in `config.py` with your MySQL credentials:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "your_mysql_username",
    "password": "your_mysql_password",
    "database": "qr"
}
```

3. Execute the database setup script:

```bash
# Login to MySQL
mysql -u your_username -p

# Inside MySQL, run the queries from db.queries.txt
# You can either copy-paste the contents or use the source command:
source path/to/db.queries.txt
```

Alternatively, you can use MySQL Workbench or other GUI tools to execute the SQL script.

### Step 4: Run the Application

```bash
python app.py
```

The application will be accessible at `http://localhost:5000`

## Usage

1. **Home Page**: Access the main page to scan QR codes
2. **Scanning**: Upload a QR code image to scan products
3. **Cart**: View your cart and adjust quantities as needed
4. **Checkout**: Proceed to checkout to complete your purchase
5. **Add Products**: Use the admin page to add new products

## Generating QR Codes for Products

You can generate QR codes for products using the included utility:

```bash
python generate_qr.py
```

This will create QR codes for products in the database that can be scanned by the application.

## Troubleshooting

### Database Connection Issues

- Ensure your MySQL server is running
- Verify the credentials in `config.py` match your MySQL setup
- Check that the database 'qr' has been created

### Package Installation Problems

If you encounter issues with the `mysqlclient` package installation:

- **Windows**: You might need to install the appropriate Visual C++ Build Tools
- **macOS**: You might need to install MySQL via brew: `brew install mysql`
- **Linux**: You might need to install development libraries: `sudo apt-get install python3-dev default-libmysqlclient-dev build-essential`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
