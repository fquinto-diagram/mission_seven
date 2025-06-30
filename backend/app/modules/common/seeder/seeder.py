import argparse
from app.config.database import SessionLocal
from app.modules.users.seeders.user_seeder import UserSeeder
from app.modules.roles.seeders.role_seeder import RoleSeeder
from app.modules.roles.seeders.permission_seeder import PermissionSeeder
from app.modules.countries.seeders.country_seeder import CountrySeeder
from app.modules.countries.seeders.province_seeder import ProvinceSeeder
from app.modules.companies.seeders.company_seeder import CompanySeeder

def run(refresh=False):
    db = SessionLocal()
    try:
        if refresh:
            print("🔄 Opción --refresh detectada. Limpiando tablas...")
            RoleSeeder.truncate(db)
            UserSeeder.truncate(db)
            PermissionSeeder.truncate(db)
            CountrySeeder.truncate(db)
            ProvinceSeeder.truncate(db)
            CompanySeeder.truncate(db)

        RoleSeeder.run(db)
        UserSeeder.run(db)
        PermissionSeeder.run(db)
        CountrySeeder.run(db)
        ProvinceSeeder.run(db)
        CompanySeeder.run(db)
        
        print("""
              --------------------------------
              ✅ Database seeded successfully
              --------------------------------
              """)
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the database.")
    parser.add_argument(
        "--refresh", action="store_true", help="Delete all data and seed from scratch"
    )
    args = parser.parse_args()
    run(refresh=args.refresh)
