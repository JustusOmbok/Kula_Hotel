import unittest
import tempfile
from datetime import datetime
import os
from flask import Flask
from app import app, db
from app.models import Guest, Room, Booking

class BookingTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for the SQLite database
        self.db_fd, app.config['SQLALCHEMY_DATABASE_URI'] = tempfile.mkstemp()

        # Set up a Flask test app and configure it for testing
        self.app = app.test_client()
        self.app.application.config['TESTING'] = True

        # Use the SQLAlchemy instance from the main application
        self.db = db

        # Create the database tables
        with self.app.application.app_context():
            self.db.create_all()

        # Clear existing data in the database
        self.clear_database()

        self.db = db

        # Clear existing data in the database
        self.clear_database()

        # Create the database tables
        with self.app.application.app_context():
            self.db.create_all()

        # Create a booking for testing
        with self.app.application.app_context():
            self.create_test_booking()

    def tearDown(self):
        # Clean up the database and remove the temporary file after each test
        os.close(self.db_fd)
        os.unlink(app.config['SQLALCHEMY_DATABASE_URI'])

    def clear_database(self):
        with self.app.application.app_context():
            # Clear all data from tables
            self.db.session.query(Guest).delete()
            self.db.session.query(Room).delete()
            self.db.session.query(Booking).delete()

            # Commit the changes
            self.db.session.commit()

    def create_test_booking(self):

        # Define the data for creating a booking
        booking_data = {
            'guest': {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'testuser_8@example.com',
                'phone': '1234567890'
            },
            'room': {
                'room_number': '101',
                'room_type': 'Standard',
                'price_per_night': 100.0
            },
            'check_in_date': '2023-01-01',  # Update the date format
            'check_out_date': '2023-01-05',
            'total_price': 400.0
        }

        # Send a POST request to the API endpoint to create a booking
        response = self.app.post('/api/bookings', json=booking_data)

        # Commit the changes to the database
        self.db.session.commit()

    def test_get_bookings(self):
        # Send a GET request to the API endpoint to retrieve bookings
        response = self.app.get('/api/bookings')

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the expected data (you can modify this based on your actual data)
        expected_data = [
            {
                'id': 1,
                'guest': {
                    'id': 1,
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'testuser_8@example.com',
                    'phone': '1234567890',
                },
                'room': {
                    'id': 1,
                    'room_number': '101',
                    'room_type': 'Standard',
                    'price_per_night': 100.0,
                },
                'check_in_date': '2023-01-01T00:00:00',  # Update the date format
                'check_out_date': '2023-01-05T00:00:00',
                'total_price': 400.0,
            }
            # Add more entries as needed
        ]

        # Parse the response as JSON
        response_data = response.get_json()

        # Check if the response contains the expected data (order doesn't matter)
        print("Response Data:")
        print(response_data)

        print("Expected Data:")
        print(expected_data)

        # Check if the response data matches the expected data (order doesn't matter)
        self.assertCountEqual(response_data, expected_data)

if __name__ == '__main__':
    unittest.main()
