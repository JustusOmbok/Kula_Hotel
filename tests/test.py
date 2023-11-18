import unittest
from app import app, db
from datetime import datetime, timedelta
from app.models import Booking, Guest, Room


class TestKulaHotelApp(unittest.TestCase):
    def setUp(self):
        # Set up the app for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel_test.db'  # Use a different database for testing
        self.app = app.test_client()

        with app.app_context():
            # Initialize SQLAlchemy only if not already initialized
            if not hasattr(app, 'extensions') or 'sqlalchemy' not in app.extensions:
                db.init_app(app)
                db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_database_connection(self):
        with app.app_context():
            # Create tables explicitly before adding data
            db.create_all()  # Ensure that tables are created

            # Ensure that the database connection is established
            # Add a dummy record to test the connection
            guest = Guest(first_name='Test', last_name='User', email='test@example.com', phone='123456789')
            db.session.add(guest)
            db.session.commit()

            # Retrieve the dummy record
            retrieved_guest = Guest.query.filter_by(email='test@example.com').first()

            self.assertIsNotNone(retrieved_guest)
            self.assertEqual(retrieved_guest.first_name, 'Test')

if __name__ == '__main__':
    unittest.main()