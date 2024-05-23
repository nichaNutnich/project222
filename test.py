from models import db, Court, Time
from app import app

with app.app_context():
    db.create_all()

    courts = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10']
    times = ['17:00-18:00', '18:00-19:00', '19:00-20:00', '20:00-21:00', '21:00-22:00']

    for court_name in courts:
        court = Court(name=court_name)
        db.session.add(court)

    for time_range in times:
        time = Time(time_range=time_range)
        db.session.add(time)

    db.session.commit()
