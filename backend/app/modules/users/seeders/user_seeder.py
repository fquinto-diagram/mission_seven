from sqlalchemy.orm import Session
from app.modules.users.models import User
from app.modules.auth.models import ResetPasswordToken
import bcrypt
from app.modules.roles.models.role_model import Role

class UserSeeder:
    
    @staticmethod
    def run(db: Session):
        if db.query(User).count() == 0:
            users = [
                User(
                    name="David",
                    surname="Super Admin",
                    email="dfalco@dsdiagram.es",
                    password=bcrypt.hashpw(b"password", bcrypt.gensalt()).decode("utf-8"),
                    lang='es'
                ),
                User(
                    name="Gabriel",
                    surname="Super Admin",
                    email="gabriel@diagram.es",
                    password=bcrypt.hashpw(b"password", bcrypt.gensalt()).decode("utf-8"),
                    lang='es'
                )
            ]
            db.add_all(users)
            db.commit()
            users = db.query(User).all()
            for user in users:
                user.roles = [db.query(Role).filter(Role.name == "Super Admin").first()]
                db.commit()
            print("[users] Table seeded successfully✅ ")
        else:
            print("[users] Table already seeded. No new users created.")
            
    @staticmethod
    def truncate(db: Session):
        db.query(ResetPasswordToken).delete()
        db.query(User).delete()
        db.commit()
        print("[users] Table truncated successfully✅ ")
    