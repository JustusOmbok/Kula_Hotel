from flask import render_template, request, jsonify, session, redirect, url_for
from app import app, db
from datetime import datetime
from app.models import Booking, Guest, Room, User
# Home Page
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/booking/dashboard')
def booking_dashboard():
    return render_template('booking_dashboard.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/staff/dashboard')
def staff_dashboard():
    return render_template('staff_dashboard.html')

@app.route('/user/dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/create_booking', methods=['GET'])
def render_create_booking():
    return render_template('create_booking.html')

@app.route('/add_room', methods=['GET'])
def render_add_room():
    return render_template('add_room.html')

@app.route('/delete_booking', methods=['GET'])
def render_delete_booking():
    return render_template('delete_booking.html')

@app.route('/get_all_bookings', methods=['GET'])
def render_get_all_bookings():
    return render_template('get_all_bookings.html')

@app.route('/get_booking_by_id', methods=['GET'])
def render_get_booking_by_id():
    return render_template('get_booking_by_id.html')

@app.route('/update_booking', methods=['GET'])
def render_update_booking():
    return render_template('update_booking.html')

@app.route('/staff/signup')
def signup():
    return render_template('signup.html')

@app.route('/staff/login')
def render_login():
    return render_template('login.html')

# RESTful API for Booking
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    # Fetch all bookings from the database and return as JSON
    bookings = Booking.query.all()
    # Serialize bookings with booking ID included
    serialized_bookings = [{'id': booking.id, **booking.serialize()} for booking in bookings]
    return jsonify(serialized_bookings)

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

    room = Room.query.filter_by(room_number=data['room']['room_number']).first()
    
    if room and room.available:
        booking = Booking(
            guest=guest,
            room=room,
            check_in_date=datetime.strptime(data['check_in_date'], "%Y-%m-%d"),
            check_out_date=datetime.strptime(data['check_out_date'], "%Y-%m-%d"),
            total_price=data['total_price']
        )

        # Mark the room as booked
        room.mark_as_booked()

        db.session.add(guest)
        db.session.add(booking)
        db.session.commit()

        # Return the booking ID along with the success message
        booking_id = booking.id
        return jsonify({'message': 'Booking created successfully', 'booking_id': booking_id}), 201
    else:
        return jsonify({'error': 'Room not available or does not exist'}), 400

@app.route('/api/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    data = request.get_json()
    booking = Booking.query.get(booking_id)
    
    if booking:
        # Convert the 'check_out_date' string to a datetime object
        data['check_out_date'] = datetime.strptime(data['check_out_date'], "%Y-%m-%d")
        data['check_in_date'] = datetime.strptime(data['check_in_date'], "%Y-%m-%d")
        # Update the booking and return it as JSON
        for key, value in data.items():
            setattr(booking, key, value)
        db.session.commit()
        return jsonify({'message': 'Booking updated successfully'}), 201
    
    return jsonify({'error': 'Booking not found'}), 404

@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        # Mark the room as available
        booking.room.mark_as_available()

        # Delete the booking
        db.session.delete(booking)
        db.session.commit()
        return jsonify({'message': 'Booking deleted'})
    return jsonify({'error': 'Booking not found'}), 404

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()

    new_user = User(
        username=data['username'],
        password=data['password']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    else:
        # Handle GET request (e.g., return a login page)
        return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    with app.app_context():
        session.pop('user_id', None)
        return jsonify({'message': 'Logout successful', 'success': True}), 200
    
@app.route('/logout', methods=['GET'])  # This could be 'GET' instead of 'POST' since you are only redirecting
def render_logout():
    return render_template('logout.html')
    
@app.route('/api/rooms', methods=['POST'])
def add_room():
    data = request.get_json()

    new_room = Room(
        room_number=data['room_number'],
        room_type=data['room_type'],
        price_per_night=data['price_per_night'],
        available=True  # New room is initially available
    )

    db.session.add(new_room)
    db.session.commit()

    return jsonify({'message': 'Room added successfully', 'success': True}), 201


@app.route('/api/available_rooms', methods=['GET'])
def get_available_rooms():
    room_type = request.args.get('room_type')

    if room_type:
        available_rooms = Room.query.filter_by(room_type=room_type, available=True).all()
        response_data = [{'room_number': room.room_number, 'price_per_night': room.price_per_night} for room in available_rooms]
        return jsonify(response_data)

    return jsonify({'error': 'Invalid request'}), 400

@app.route('/api/room_price', methods=['GET'])
def get_room_price():
    room_number = request.args.get('room_number')

    if room_number:
        room = Room.query.filter_by(room_number=room_number).first()
        if room:
            return jsonify({'price_per_night': room.price_per_night})

    return jsonify({'error': 'Invalid room number'}), 400
