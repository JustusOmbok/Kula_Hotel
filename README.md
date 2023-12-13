Kula Hotel Booking System

Site Deployed
http://54.160.76.99/

Overview
The Kula Hotel Booking System is a web application built with Flask, a Python web framework. It provides a user-friendly interface for both guests and staff members to manage hotel bookings, add rooms, and perform various booking-related actions.

Features
User Authentication:
Secure user authentication system for login and signup.
Staff and user dashboards with relevant actions.

Booking Management:
Create, update, and delete bookings.
Retrieve bookings by ID or get a list of all bookings.

Room Management:
Add new rooms with details like room number, type, and price per night.
Dynamically calculate total price based on room type and selected dates.

Logout:
Allow users to log out securely.

Licensing
© 2023 Kula Hotel. All rights reserved.

Technologies Used
Flask: Web framework used for building the application.
HTML, CSS, JavaScript: Front-end technologies for designing and enhancing user interfaces.
Fetch API: Used for making asynchronous requests to the server.

Project Structure
├── app/
│   ├── static/
│   │   ├── styles1.css
│   │   ├── styles3.css
│   │   ├── styles6.css
│   │   ├── styles7.css
│   │   ├── styles9.css
│   │   ├── styles10.css
│   │   ├── styles11.css
│   ├── templates/
│   │   ├── add_room.html
│   │   ├── booking_dashboard.html
│   │   ├── create_booking.html
│   │   ├── delete_booking.html
│   │   ├── get_all_bookings.html
│   │   ├── get_booking_by_id.html
│   │   ├── homepage.html
│   │   ├── login.html
│   │   ├── logout.html
│   │   ├── signup.html
│   │   ├── staff_dashboard.html
│   │   ├── update_booking.html
│   │   ├── user_dashboard.html
├── run.py
├── requirements.txt
├── config.py
├── README.md

Setup
Clone the repository:
git clone https://github.com/your-username/kula-hotel-booking-system.git
cd kula-hotel-booking-system

Install dependencies:
pip install -r requirements.txt

Run the application:
python run.py
Visit http://localhost:5000 in your web browser to access the application.

Usage
Access the homepage to view hotel details and available rooms.
Use the staff dashboard for staff-related actions.
Navigate to the user dashboard for user-specific actions.
Explore different functionalities such as creating, updating, and deleting bookings.

Authors
Justus Ombok: https://github.com/JustusOmbok
Sandra Mauku: https://github.com/sendyTheDev

Contributing
Contributions are welcome! If you find any issues or have suggestions, please open an issue or submit a pull request.

License
This project is licensed under the MIT License.


