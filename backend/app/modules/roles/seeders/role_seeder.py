from app.modules.roles.models.role_model import Role
from sqlalchemy.orm import Session

class RoleSeeder:
    
    
    @staticmethod
    def run(db: Session):
        if db.query(Role).count() == 0:
            db.add(Role(name="Super Admin"))
            db.commit()
            print("[roles] Table seeded successfully✅ ")
        else:
            print("[roles] Table already seeded")

    @staticmethod
    def truncate(db: Session):
        db.query(Role).delete()
        db.commit()
        print("[roles] Table truncated successfully✅ ")
