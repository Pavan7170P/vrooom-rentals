from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
import bcrypt  # Import bcrypt for password hashing

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a strong secret key

# ✅ Database Connection
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",   # XAMPP MySQL
        user="root",        # Default XAMPP MySQL user
        password="",        # Default MySQL has no password
        database="car_rental"  # Your database name
    )
    return conn

# ✅ Admin Credentials (Hardcoded for now)
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin123"  # Change this to a strong password

# ✅ Render Admin Login Page
@app.route('/admin_login')
def admin_login_page():
    return render_template('admin_login.html')

# ✅ Handle Admin Login
@app.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.form['email']
    password = request.form['password']

    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        session['admin'] = True  # Set admin session
        return redirect(url_for('admin_dashboard'))
    else:
        return jsonify({"message": "Invalid admin credentials"}), 401

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

# ✅ Admin Dashboard (Manage Bookings, Cars, Availability)
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login_page'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch all bookings
    cursor.execute("""
        SELECT bookings.id, users.name AS user_name, cars.name AS car_name, 
               bookings.days, payments.amount, payments.status
        FROM bookings
        JOIN users ON bookings.user_id = users.id
        JOIN cars ON bookings.car_id = cars.id
        LEFT JOIN payments ON bookings.id = payments.booking_id
    """)
    bookings = cursor.fetchall()

    # Fetch all cars
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()

    conn.close()

    return render_template('admin_dashboard.html', bookings=bookings, cars=cars)

# ✅ Update Payment Status (Admin Only)
@app.route('/update_payment/<int:booking_id>', methods=['POST'])
def update_payment(booking_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login_page'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE payments SET status = 'Paid' WHERE booking_id = %s", (booking_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('admin_dashboard'))

# ✅ Add a New Car (Admin Only)
@app.route('/add_car', methods=['POST'])
def add_car():
    if 'admin' not in session:
        return redirect(url_for('admin_login_page'))

    car_name = request.form['name']
    price_per_day = request.form['price_per_day']
    image_url = request.form['image_url']
    availability = request.form['availability']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cars (name, price_per_day, image_url, availability) VALUES (%s, %s, %s, %s)", 
                   (car_name, price_per_day, image_url, availability))
    conn.commit()
    conn.close()

    return redirect(url_for('admin_dashboard'))

# ✅ Remove a Car (Admin Only)
@app.route('/remove_car/<int:car_id>', methods=['POST'])
def remove_car(car_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login_page'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cars WHERE id = %s", (car_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('admin_dashboard'))

# ✅ Update Car Details (Admin Only)
@app.route('/update_car/<int:car_id>', methods=['POST'])
def update_car(car_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login_page'))

    price_per_day = request.form.get('price_per_day')  # Optional price
    availability = request.form.get('availability')  # Always required

    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ Update only the provided fields
    if price_per_day:
        cursor.execute("UPDATE cars SET price_per_day = %s, availability = %s WHERE id = %s", 
                       (price_per_day, availability, car_id))
    else:
        cursor.execute("UPDATE cars SET availability = %s WHERE id = %s", (availability, car_id))

    conn.commit()
    conn.close()

    return redirect(url_for('admin_dashboard'))


# ✅ Home Route - Fetch Available Cars
@app.route('/')
def home():
    return render_template('index.html')  # Home page without cars listing


@app.route('/logout')
def logout():
    session.clear()  # ✅ Clears the entire session
    return redirect(url_for('home'))

# ✅ Render Login Page (GET) and Handle Login (POST)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  # Show login page

    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    conn.close()

    # ✅ Fix: Verify Hashed Password Correctly
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):  
        session['user_id'] = user['id']  # Store user ID in session
        return redirect(url_for('home'))  # Redirect to home page
    else:
        return jsonify({"message": "Invalid credentials, try again."}), 401

# ✅ Render Registration Page (GET & POST)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # ✅ Ensure Password is Hashed Before Storing
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if email already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return jsonify({"message": "Email already registered!"}), 400

    # Store hashed password in MySQL
    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
    conn.commit()
    conn.close()

    return redirect(url_for('login'))  # ✅ Redirects to login page

# ✅ Confirm Booking & Store Payment Details
@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    car_id = request.form['car_id']
    days = int(request.form['days'])
    amount = float(request.form['amount'])  # Get total price
    payment_method = request.form.get('payment_method', 'Pay at Location')
    location = request.form.get('location')  # ✅ Get selected location
    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ Insert booking into database (including location)
    cursor.execute("INSERT INTO bookings (user_id, car_id, days, location) VALUES (%s, %s, %s, %s)", 
                   (user_id, car_id, days, location))
    booking_id = cursor.lastrowid  # Get last inserted booking ID

    # ✅ Insert payment details into `payments` table
    cursor.execute("INSERT INTO payments (booking_id, user_id, amount, payment_method, status) VALUES (%s, %s, %s, %s, 'Pending')",
                   (booking_id, user_id, amount, payment_method))
    
    conn.commit()
    conn.close()

    return redirect(url_for('booking_success'))



# ✅ Booking Success Page
@app.route('/booking_success')
def booking_success():
    return render_template('booking_success.html')


# ✅ Render Booking Page (User must be logged in)
@app.route('/book/<int:car_id>')
def book_page(car_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
    car = cursor.fetchone()
    conn.close()

    if not car:
        return "Car not found", 404

    return render_template('book.html', car=car)

# ✅ Render cars availability page (User must be logged in)
@app.route('/view_cars')
def view_cars():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch Available and Unavailable Cars
    cursor.execute("SELECT * FROM cars WHERE availability = 'Available'")
    available_cars = cursor.fetchall()

    cursor.execute("SELECT * FROM cars WHERE availability = 'Not Available'")
    unavailable_cars = cursor.fetchall()
    
    conn.close()

    return render_template('view_cars.html', available_cars=available_cars, unavailable_cars=unavailable_cars)



# ✅ About Page Route
@app.route('/about')
def about():
    return render_template('about.html')

# ✅ Contact Page Route
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
