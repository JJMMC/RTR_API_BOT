from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# Configurar la base de datos
engine = create_engine('sqlite:///database/rtr_crawler_Alchemy.db')
Session = sessionmaker(bind=engine)

def get_session():
    session = Session()
    try:
        return session
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

# Crear todas las tablas en la base de datos
#Base.metadata.create_all(engine)