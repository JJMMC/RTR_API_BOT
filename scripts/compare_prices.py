from sqlalchemy import select, join, delete
from scripts.dbsetup import get_session
from app.models import Articulo, HistorialPrecio


def get_ultimas_fechas():
    session = get_session()
    try:
        stmt = select(HistorialPrecio.fecha).distinct().order_by(HistorialPrecio.fecha.desc()).limit(2)
        result = session.execute(stmt).scalars().all()
        return result
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


def get_precios_por_fecha(fecha):
    session = get_session()
    try:
        stmt = select(HistorialPrecio.rtr_id,HistorialPrecio.precio,Articulo.nombre,Articulo.categoria).select_from(
            join(HistorialPrecio, Articulo, HistorialPrecio.rtr_id == Articulo.rtr_id)
        ).where(HistorialPrecio.fecha == fecha)
        result = session.execute(stmt).all()
        return result
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


def comparar_precio_fechas():
    fechas = get_ultimas_fechas()
    if len(fechas) < 2:
        print ("Fechas insuficientes")
        return
    print(fechas)
    ultima_fecha, penultima_fecha = fechas
    datos_ultima_fecha = get_precios_por_fecha(ultima_fecha)
    datos_penultima_fecha = get_precios_por_fecha(penultima_fecha)

    cambios_de_precio = []
    penultima_fecha_dict = {rtr_id: (precio, nombre, categoria) for rtr_id, precio, nombre, categoria in datos_penultima_fecha}
    
    for rtr_id, ultimo_precio, nombre, categoria in datos_ultima_fecha:
        penultimo_precio, _, _ = penultima_fecha_dict.get(rtr_id, (None, None, None))
        if penultimo_precio is not None and ultimo_precio != penultimo_precio:
            cambios_de_precio.append((rtr_id, nombre, categoria, penultimo_precio, ultimo_precio))

    if cambios_de_precio:
        print(f"Cambios de precios entre {penultima_fecha} y {ultima_fecha}:")
        for rtr_id, nombre, categoria, penultimo_precio, ultimo_precio in cambios_de_precio:
            print(f"RTR ID: {rtr_id}, Nombre: {nombre}, Categoría: {categoria}, Precio anterior: {penultimo_precio}, Precio actual: {ultimo_precio}")

