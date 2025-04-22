from app.database import SessionLocal, create_tables
from app.models import User
from passlib.hash import bcrypt

def seed_admin():
    create_tables()
    db = SessionLocal()
    if not db.query(User).count():
        admin = User(
            username="superadmin",
            password_hash=bcrypt.hash("ChangeMe123!"),
            is_admin=True,
            user_type="admin"
        )
        db.add(admin)
        db.commit()
        print("Superadmin created: username=superadmin, password=ChangeMe123!")
    db.close()

if __name__ == "__main__":
    seed_admin()