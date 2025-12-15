# 🚗 Vrooom Rentals – Car Rental Management System

Vrooom Rentals is a web-based Car Rental Management System designed to automate and simplify the process of renting cars. The application allows users to browse available vehicles, book cars online, and manage rentals efficiently while following an offline payment approach.

This project aims to reduce the challenges of traditional manual car rental systems by providing structured booking management, real-time availability updates, and secure admin control.

---

## ✨ Features

### User Features
- User registration and login
- Browse available cars
- Book cars with rental duration details
- Booking confirmation
- Offline payment system (Pay at rental location)

### Admin Features
- Admin login and dashboard
- Add, update, and remove cars
- View and manage all bookings
- Update payment status after offline payment
- Monitor vehicle availability and rental history

---

## 🧱 Project Structure
vrooom-rentals/
│
├── app.py
├── script.js
│
├── static/
│ ├── cars/
│ ├── icons/
│ ├── style.css
│ └── styles.css
│
├── templates/
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── view_cars.html
│ ├── book.html
│ ├── booking_success.html
│ ├── admin_login.html
│ ├── admin_dashboard.html
│ ├── about.html
│ └── contact.html

---

## 🛠️ Tech Stack

- Frontend: HTML, CSS, JavaScript  
- Backend: Python (Flask)  
- Database: MySQL (XAMPP)

---

## ⚙️ Installation & Setup

1. Clone the repository:
git clone https://github.com/your-username/vrooom-rentals.git

2. Install required dependencies:
pip install flask mysql-connector-python

markdown
Copy code

3. Database setup:
- Start XAMPP and enable MySQL
- Create a database named `car_rental`
- Import the SQL file if provided

4. Run the application:
python app.py

markdown
Copy code

5. Open in browser:
http://127.0.0.1:5000/

yaml
Copy code

---

## 💳 Payment Model

This system follows an offline payment model:
- Users book cars online
- Payment is made at the rental location
- Admin updates the payment status manually

This ensures accurate transaction tracking without using online payment gateways.

---

## 🔐 Security & Access Control

- User authentication is required before booking
- Admin access is restricted
- Prevents unauthorized bookings and maintains data integrity

---

## 📌 Purpose

This project is suitable for:
- Academic and college projects
- Portfolio and resume showcase
- Learning full-stack development using Flask and MySQL

---

## 📄 License

This project is developed for educational and portfolio purposes only.
