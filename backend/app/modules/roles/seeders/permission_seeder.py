from sqlalchemy.orm import Session
from app.modules.roles.models.permission_model import Permission
from app.modules.roles.models.role_model import Role

class PermissionSeeder:
    
    @staticmethod
    def run(db: Session):
        if db.query(Permission).count() == 0:
            permissions = [
                "accounting_accounts.can.delete",
                "accounting_accounts.can.manage",
                "accounting_accounts.can.view",
                "budgets.can.delete",
                "budgets.can.manage",
                "budgets.can.view",
                "clients.can.delete",
                "clients.can.manage",
                "clients.can.view",
                "companies.can.delete",
                "companies.can.manage",
                "companies.can.view",
                "einvoice_payment_types.can.delete",
                "einvoice_payment_types.can.manage",
                "einvoice_payment_types.can.view",
                "expenses.can.delete",
                "expenses.can.manage",
                "expenses.can.view",
                "invoice_serie_types.can.delete",
                "invoice_serie_types.can.manage",
                "invoice_serie_types.can.view",
                "invoice_series.can.delete",
                "invoice_series.can.manage",
                "invoice_series.can.view",
                "iva_types.can.delete",
                "iva_types.can.manage",
                "iva_types.can.view",
                "payment_forms.can.delete",
                "payment_forms.can.manage",
                "payment_forms.can.view",
                "person_types.can.delete",
                "person_types.can.manage",
                "person_types.can.view",
                "products.can.delete",
                "products.can.manage",
                "products.can.view",
                "providers.can.delete",
                "providers.can.manage",
                "providers.can.view",
                "purchases_invoices.can.delete",
                "purchases_invoices.can.manage",
                "purchases_invoices.can.view",
                "purchases_recipts.can.delete",
                "purchases_recipts.can.manage",
                "purchases_recipts.can.view",
                "roles.can.delete",
                "roles.can.manage",
                "roles.can.view",
                "sales_invoices.can.delete",
                "sales_invoices.can.manage",
                "sales_invoices.can.view",
                "sales_recipts.can.delete",
                "sales_recipts.can.manage",
                "sales_recipts.can.view",
                "users.can.delete",
                "users.can.manage",
                "users.can.view",
            ]
            super_admin_role = db.query(Role).filter(Role.name == "Super Admin").first()

            permissions_objs = []

            for name in permissions:
                permission = Permission(name=name)
                db.add(permission)
                permissions_objs.append(permission)
            db.commit()

            for permission in db.query(Permission).filter(Permission.name.in_(permissions)).all():
                super_admin_role.permissions.append(permission)
            db.commit()
            print("[permissions] Table seeded successfully✅ ")
        else:
            print("[permissions] Table already seeded")

    @staticmethod
    def truncate(db: Session):
        db.query(Permission).delete()
        db.commit()
        print("[permissions] Table truncated successfully✅ ")
