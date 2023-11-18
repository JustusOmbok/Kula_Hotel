from flask import render_template, request, jsonify
from app import app, db
from datetime import datetime
from app.models import Booking, Guest, Room

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# RESTful API for Booking
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    # Fetch all bookings from the database and return as JSON
    bookings = Booking.query.all()
    return jsonify([booking.serialize() for booking in bookings])

@app.route('/api/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    # Fetch a specific booking by ID and return as JSON
    booking = Booking.query.get(booking_id)
    if booking:
        return jsonify(booking.serialize())
    return jsonify({'error': 'Booking not found'}), 404

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()

    guest = Guest(
        first_name=data['guest']['first_name'],
        last_name=data['guest']['last_name'],
        email=data['guest']['email'],
        phone=data['guest']['phone']
    )

    room = Room(
        room_number=data['room']['room_number'],
        room_type=data['room']['room_type'],
        price_per_night=data['room']['price_per_night']
    )

    booking = Booking(
        guest=guest,
        room=room,
        check_in_date=datetime.strptime(data['check_in_date'], "%Y-%m-%d"),
        check_out_date=datetime.strptime(data['check_out_date'], "%Y-%m-%d"),
        total_price=data['total_price']
    )

    db.session.add(guest)
    db.session.add(room)
    db.session.add(booking)
    db.session.commit()

    return jsonify({'message': 'Booking created successfully'}), 201

@app.route('/api/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    data = request.get_json()
    booking = Booking.query.get(booking_id)
    if booking:
        # Update the booking and return it as JSON
        for key, value in data.items():
            setattr(booking, key, value)
        db.session.commit()
        return jsonify(booking.serialize())
    return jsonify({'error': 'Booking not found'}), 404

@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        # Delete the booking
        db.session.delete(booking)
        db.session.commit()
        return jsonify({'message': 'Booking deleted'})
    return jsonify({'error': 'Booking not found'}), 404