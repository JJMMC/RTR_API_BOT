from sqlalchemy import select, join, delete
from scripts.dbsetup import get_session
from app.models import Articulo, HistorialPrecio


### FUNCIONES SELECT ###

# Leer todo de tabla articulos y printea algunos datos
def leer_tabla():
    session = get_session()
    try:
        stmt = select(Articulo)
        result = session.execute(stmt)
        for user_obj in result.scalars():
            print(f"{user_obj.nombre} {user_obj.rtr_id}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

# Leer tabla ordenada por rtr_id
def leer_tabla_ordenada():
    session = get_session()
    try:
        stmt = select(Articulo).order_by(Articulo.rtr_id)
        result = session.execute(stmt)
        for data in result.scalars():
            print(f"{data.nombre} {data.rtr_id}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

# Consultas con JOIN
def leer_historial_precios_con_nombre():
    session = get_session()
    try:
        stmt = select(HistorialPrecio, Articulo.nombre).select_from(
            join(HistorialPrecio, Articulo, HistorialPrecio.rtr_id == Articulo.rtr_id)
        )
        result = session.execute(stmt)
        for historial, nombre in result:
            print(f"Artículo: {nombre}, RTR ID: {historial.rtr_id}, Precio: {historial.precio}, Fecha: {historial.fecha}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

def leer_historial_precios_con_nombre_y_categoria():
    session = get_session()
    try:
        stmt = select(HistorialPrecio, Articulo.nombre, Articulo.categoria).select_from(
            join(HistorialPrecio, Articulo, HistorialPrecio.rtr_id == Articulo.rtr_id)
        )
        result = session.execute(stmt)
        for historial, nombre, categoria in result:
            print(f"Artículo: {nombre}, Categoría: {categoria}, RTR ID: {historial.rtr_id}, Precio: {historial.precio}, Fecha: {historial.fecha}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

# Filtrar Tabla Articulos por categoría
def obtener_articulos_por_categoria(categoria):
    session = get_session()
    try:
        stmt = select(Articulo).where(Articulo.categoria == categoria)
        result = session.execute(stmt).scalars().all()
        
        return result
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


### NUEVA FUNCIÓN PARA ELIMINAR FILAS POR FECHA ###
def delete_rows_by_date(fecha):
    session = get_session()
    try:
        stmt = delete(HistorialPrecio).where(HistorialPrecio.fecha == fecha)
        result = session.execute(stmt)
        session.commit()
        print(f"Se eliminaron {result.rowcount} filas con la fecha {fecha}")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()
