import os
import unittest
import tempfile
from app import app, db
from app.models import Guest, Room, Booking


class FlaskAppTests(unittest.TestCase):

    import os
import unittest
import tempfile
from app import app, db

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        # Set up a temporary SQLite database for testing
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the temporary database
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_home_page(self):
        with app.app_context():
            response = self.app.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Kula_Hotel', response.data)

    def test_get_bookings(self):
        # Test the endpoint to fetch all bookings
        with app.app_context():
            response = self.app.get('/api/bookings')
            self.assertEqual(response.status_code, 200)

    def test_get_booking(self):
        # Test the endpoint to fetch a specific booking
        with app.app_context():
            booking = Booking(guest=Guest(), room=Room(), check_in_date='2023-01-01', check_out_date='2023-01-02', total_price=100.0)
            db.session.add(booking)
            db.session.commit()

            response = self.app.get(f'/api/bookings/{booking.id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['id'], booking.id)

    def test_create_booking(self):
        with app.app_context():
            data = {
            "guest": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "123-456-7890"
            },
            "room": {
                "room_number": "101",
                "room_type": "Standard",
                "price_per_night": 100.0
            },
            "check_in_date": "2023-01-01",
            "check_out_date": "2023-01-02",
            "total_price": 100.0
        }

        response = self.app.post('/api/bookings', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Booking created', response.data)

        response = self.app.post('/api/bookings', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Booking created', response.data)

    def test_update_booking(self):
        with app.app_context():
        # Test the endpoint to update a booking
            booking = Booking(guest=Guest(first_name="John", last_name="Doe", email="john.doe@example.com", phone="123-456-7890"),
                          room=Room(room_number="101", room_type="Standard", price_per_night=100.0),
                          check_in_date='2023-01-01', check_out_date='2023-01-02', total_price=100.0)
            db.session.add(booking)
            db.session.commit()

            updated_data = {
                "guest": {
                    "first_name": "UpdatedFirstName",
                    "last_name": "UpdatedLastName",
                    "email": "updated.email@example.com",
                    "phone": "987-654-3210"
                },
                "room": {
                    "room_number": "102",
                    "room_type": "Deluxe",
                    "price_per_night": 150.0
                },
                "check_in_date": "2023-02-01",
                "check_out_date": "2023-02-03",
            "total_price": 150.0
        }

        response = self.app.put(f'/api/bookings/{booking.id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Booking updated', response.data)

    def test_delete_booking(self):
        with app.app_context():
            # Test the endpoint to delete a booking
            guest = Guest(first_name="John", last_name="Doe", email="john.doe@example.com", phone="123-456-7890")
            room = Room(room_number="101", room_type="Standard", price_per_night=100.0)
            booking = Booking(guest=guest, room=room, check_in_date='2023-01-01', check_out_date='2023-01-02', total_price=100.0)
            db.session.add(guest)
            db.session.add(room)
            db.session.add(booking)
            db.session.commit()

            response = self.app.delete(f'/api/bookings/{booking.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Booking deleted', response.data)


if __name__ == '__main__':
    unittest.main()
