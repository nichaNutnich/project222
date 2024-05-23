from flask import Flask, request, jsonify
from models import db, User, Court, Time
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

    # เพิ่มข้อมูลคอร์ทและเวลาถ้ายังไม่มี
    if not Court.query.first():
        courts = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10']
        for court_name in courts:
            new_court = Court(name=court_name)
            db.session.add(new_court)
        db.session.commit()

    if not Time.query.first():
        times = ['17.00-18.00', '18.00-19.00', '19.00-20.00', '20.00-21.00', '21.00-22.00']
        for time_range in times:
            new_time = Time(time_range=time_range)
            db.session.add(new_time)
        db.session.commit()

@app.route('/users', methods=['POST'])
def add_user():
    customer_date = request.args.get('customer_date')
    customer_time = request.args.get('customer_time')
    customer_court = request.args.get('customer_court')
    customer_name = request.args.get('customer_name')
    customer_number = request.args.get('customer_number')

    try:
        customer_date = datetime.strptime(customer_date, '%Y-%m-%d').date()
        customer_time = int(customer_time)
        customer_court = int(customer_court)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    existing_booking = User.query.filter_by(customer_date=customer_date, customer_time=customer_time, customer_court=customer_court).first()
    if existing_booking:
        return jsonify({'error': 'Court is already booked for the given date and time'}), 400

    new_user = User(
        customer_date=customer_date,
        customer_time=customer_time,
        customer_court=customer_court,
        customer_name=customer_name,
        customer_number=customer_number
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully', 'user': {
            'customer_date': str(new_user.customer_date),
            'customer_time': new_user.customer_time,
            'customer_court': new_user.customer_court,
            'customer_name': new_user.customer_name,
            'customer_number': new_user.customer_number
        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
def new_court():
    new_court = Court(
         id = 1 ,name = "A01"
    )
    db.session.add(new_court)
    db.session.commit() 

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            'customer_date': str(user.customer_date),
            'customer_time': user.customer_time,
            'customer_court': user.customer_court,
            'customer_name': user.customer_name,
            'customer_number': user.customer_number
        })
    return jsonify(user_list)

if __name__ == '__main__':
    new_court()
    app.run(debug=True)
