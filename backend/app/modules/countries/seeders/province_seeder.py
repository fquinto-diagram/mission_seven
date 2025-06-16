from app.modules.countries.models.province_model import Province
from app.modules.countries.models.country_model import Country
from sqlalchemy.orm import Session

class ProvinceSeeder:
    
    @staticmethod
    def run(db: Session):
        provinces = [
            {"name": "Álava", "postcode": "01"},
            {"name": "Albacete", "postcode": "02"},
            {"name": "Alicante", "postcode": "03"},
            {"name": "Almería", "postcode": "04"},
            {"name": "Ávila", "postcode": "05"},
            {"name": "Badajoz", "postcode": "06"},
            {"name": "Islas Baleares", "postcode": "07"},
            {"name": "Barcelona", "postcode": "08"},
            {"name": "Burgos", "postcode": "09"},
            {"name": "Cáceres", "postcode": "10"},
            {"name": "Cádiz", "postcode": "11"},
            {"name": "Cantabria", "postcode": "39"},
            {"name": "Castellón", "postcode": "12"},
            {"name": "Ciudad Real", "postcode": "13"},
            {"name": "Córdoba", "postcode": "14"},
            {"name": "A Coruña", "postcode": "15"},
            {"name": "Cuenca", "postcode": "16"},
            {"name": "Girona", "postcode": "17"},
            {"name": "Granada", "postcode": "18"},
            {"name": "Guadalajara", "postcode": "19"},
            {"name": "Guipúzcoa", "postcode": "20"},
            {"name": "Huelva", "postcode": "21"},
            {"name": "Huesca", "postcode": "22"},
            {"name": "Jaén", "postcode": "23"},
            {"name": "León", "postcode": "24"},
            {"name": "Lleida", "postcode": "25"},
            {"name": "Lugo", "postcode": "27"},
            {"name": "Madrid", "postcode": "28"},
            {"name": "Málaga", "postcode": "29"},
            {"name": "Murcia", "postcode": "30"},
            {"name": "Navarra", "postcode": "31"},
            {"name": "Ourense", "postcode": "32"},
            {"name": "Palencia", "postcode": "34"},
            {"name": "Las Palmas", "postcode": "35"},
            {"name": "Pontevedra", "postcode": "36"},
            {"name": "Salamanca", "postcode": "37"},
            {"name": "Santa Cruz de Tenerife", "postcode": "38"},
            {"name": "Segovia", "postcode": "40"},
            {"name": "Sevilla", "postcode": "41"},
            {"name": "Soria", "postcode": "42"},
            {"name": "Tarragona", "postcode": "43"},
            {"name": "Teruel", "postcode": "44"},
            {"name": "Toledo", "postcode": "45"},
            {"name": "Valencia", "postcode": "46"},
            {"name": "Valladolid", "postcode": "47"},
            {"name": "Vizcaya", "postcode": "48"},
            {"name": "Zamora", "postcode": "49"},
            {"name": "Zaragoza", "postcode": "50"},
            {"name": "Ceuta", "postcode": "51"},
            {"name": "Melilla", "postcode": "52"},
        ]

        if db.query(Province).count() == 0:
            country = db.query(Country).filter(Country.iso_2_code == "ES").first()
            for province in provinces:
                db.add(Province(name=province["name"], country_id=country.id, postcode=province["postcode"]))
                db.commit()
            print("[provinces] Table seeded successfully✅ ")
        else:
            print("[provinces] Table already seeded")
        
    @staticmethod
    def truncate(db: Session):
        db.query(Province).delete()
        db.commit()