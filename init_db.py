from app import app, db
from models import User
from sqlalchemy import text
import os
from datetime import date, datetime
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        db.session.execute(text('DROP TABLE IF EXISTS users'))
        db.session.execute(text('DROP TABLE IF EXISTS options'))
        db.session.execute(text('DROP TABLE IF EXISTS questions'))
        db.session.execute(text('DROP TABLE IF EXISTS quizzes'))
        db.session.execute(text('DROP TABLE IF EXISTS results'))
        db.session.execute(text('DROP TABLE IF EXISTS option'))
        db.session.execute(text('DROP TABLE IF EXISTS question'))
        db.session.execute(text('DROP TABLE IF EXISTS quiz'))
        db.session.execute(text('DROP TABLE IF EXISTS result'))
        db.session.execute(text('DROP TABLE IF EXISTS user'))
        db.session.execute(text('DROP TABLE IF EXISTS alembic_version'))
        db.session.commit()

        db_path = os.path.join(os.path.dirname(__file__), 'instance', 'database.sqlite3')
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print("Database file deleted successfully!")
            except Exception as e:
                print(f"Error deleting database file: {e}")

        db.create_all()
        
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            admin = User(
                name='Admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                dob=datetime.strptime('2000-01-01', '%Y-%m-%d').date(),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists!")

if __name__ == '__main__':
    init_database()
    print("Database initialized successfully!") 