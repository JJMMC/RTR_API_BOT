from sqlalchemy import select, join
from scripts.dbsetup import get_session
from app.models import Articulo, HistorialPrecio
import matplotlib.pyplot as plt


def get_dos_ultimas_fechas():
    session = get_session()
    try:
        stmt = select(HistorialPrecio.fecha).distinct().order_by(HistorialPrecio.fecha.desc()).limit(2)
        result = session.execute(stmt).scalars().all()
        return result
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


def get_todos_datos_por_fecha(fecha):
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


def get_todos_datos_por_rtrid(rtr_id):
    session = get_session()
    try:
        stmt = select(
            HistorialPrecio.rtr_id,
            HistorialPrecio.precio,
            HistorialPrecio.fecha,
            Articulo.nombre,
            Articulo.categoria
            ).order_by(
                HistorialPrecio.fecha.desc()
            ).select_from(
                join(HistorialPrecio, Articulo, HistorialPrecio.rtr_id == Articulo.rtr_id)
            ).where(
                HistorialPrecio.rtr_id == rtr_id)
        
        result = session.execute(stmt).all()
        return result
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


def comparar_precio_ultimas_fechas():
    fechas = get_dos_ultimas_fechas()
    if len(fechas) < 2:
        print ("Fechas insuficientes")
        return
    print(fechas)
    ultima_fecha, penultima_fecha = fechas
    datos_ultima_fecha = get_todos_datos_por_fecha(ultima_fecha)
    datos_penultima_fecha = get_todos_datos_por_fecha(penultima_fecha)

    cambios_de_precio = []
    penultima_fecha_dict = {rtr_id: (precio, nombre, categoria) for rtr_id, precio, nombre, categoria in datos_penultima_fecha}
    
    for rtr_id, ultimo_precio, nombre, categoria in datos_ultima_fecha:
        penultimo_precio, _, _ = penultima_fecha_dict.get(rtr_id, (None, None, None))
        if penultimo_precio is not None and ultimo_precio != penultimo_precio:
            cambios_de_precio.append({
                'rtr_id': rtr_id,
                'nombre': nombre,
                'categoria': categoria,
                'penultimo_precio': penultimo_precio,
                'ultimo_precio': ultimo_precio
            })

    return cambios_de_precio
    # if cambios_de_precio:
    #     print(f"Cambios de precios entre {penultima_fecha} y {ultima_fecha}:")
    #     for rtr_id, nombre, categoria, penultimo_precio, ultimo_precio in cambios_de_precio:
    #         print(f"RTR ID: {rtr_id}, Nombre: {nombre}, Categoría: {categoria}, Precio anterior: {penultimo_precio}, Precio actual: {ultimo_precio}")


def plot_evo_precio(rtr_id):
    datos = get_todos_datos_por_rtrid(rtr_id)
    if not datos:
        print(f"No se encontraron datos para RTR ID: {rtr_id}")
        return
    else: print('\nDATOS: \n',datos)
    
    lst_fechas = [dato[2] for dato in datos]
    lst_precios = [dato[1] for dato in datos]
    print('\nFECHAS: \n',lst_fechas)
    print('\nPRECIOS: \n',lst_precios)

    plt.figure(figsize=(10, 5))
    plt.plot(lst_fechas, lst_precios, marker='o')
    plt.title(f'Evolución del precio para RTR ID: {rtr_id}')
    plt.xlabel('Fecha')
    plt.ylabel('Precio')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#####################################

def get_todos_rtrids():
    session = get_session()
    try:
        stmt = select(Articulo.rtr_id).order_by(Articulo.rtr_id.asc())
        result = session.execute(stmt).scalars().all()
        return result
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


def detectar_cambios_precio_en_historico_de_un_rtr_id(rtr_id):
    todos_datos_reg = get_todos_datos_por_rtrid(rtr_id)
    if not todos_datos_reg:
        print(f"No hay registros para RTR ID: {rtr_id}")
        return False
    
    primer_precio = todos_datos_reg[0][1]
    if primer_precio:
        #print('\nPRIMER PRECIO',primer_precio)
        #print(type(primer_precio))
        for rtr_id,precio,_ ,_ ,_ in todos_datos_reg:
            #print('Precio a COMPARAR: ',precio)
            if precio != primer_precio:
                #print('DISTINTO PRECIO')
                return True
            else: 
                continue


def detectar_cambios_precio_en_historico():
    lst_art_con_cambios = []
    for rtr_id in get_todos_rtrids():
        if detectar_cambios_precio_en_historico_de_un_rtr_id(rtr_id):
            if get_todos_datos_por_rtrid(rtr_id)[0] not in lst_art_con_cambios:
                lst_art_con_cambios.append(get_todos_datos_por_rtrid(rtr_id)[0])
        else:
            continue
    return lst_art_con_cambios




