"""Script para crear tablas en MySQL usando SQLAlchemy.
Ejecutar sólo si usas `USE_MYSQL=true` y la conexión MySQL está disponible.
"""
from config.mysql_database import engine, Base

def create_tables():
    print("Creando tablas en la base de datos MySQL...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas (si no existían).")

if __name__ == '__main__':
    create_tables()
