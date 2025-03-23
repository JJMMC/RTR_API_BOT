from app import app, db
from flask import request, jsonify, render_template
from app.models import Articulo, HistorialPrecio
from sqlalchemy import select
from scripts.dbsetup import get_session
from scripts.compare_prices import comparar_precio_ultimas_fechas, get_todos_datos_por_fecha
import matplotlib.pyplot as plt
import io
import base64


@app.route('/')
def index():
    return render_template('index.html', title="Home")


@app.route('/compare_last_prices')
def compare_last_prices():
    cambios_de_precio = comparar_precio_ultimas_fechas()
    return render_template('compare_last_prices.html', cambios_de_precio=cambios_de_precio)

@app.route('/compare_prices', methods=['GET', 'POST'])
def compare_prices():
    session = get_session()
    try:
        # Obtener todas las fechas disponibles en la base de datos
        stmt = select(HistorialPrecio.fecha).distinct().order_by(HistorialPrecio.fecha.desc())
        fechas_disponibles = [fecha[0] for fecha in session.execute(stmt).all()]

        fecha1 = None
        fecha2 = None
        cambios_de_precio = []

        if request.method == 'POST':
            # Obtener las fechas seleccionadas por el usuario
            fecha1 = request.form.get('fecha1')
            fecha2 = request.form.get('fecha2')

            if fecha1 and fecha2:
                # Comparar precios entre las dos fechas seleccionadas
                datos_fecha1 = get_todos_datos_por_fecha(fecha1)
                datos_fecha2 = get_todos_datos_por_fecha(fecha2)

                fecha1_dict = {rtr_id: (precio, nombre, categoria) for rtr_id, precio, nombre, categoria in datos_fecha1}

                for rtr_id, precio2, nombre, categoria in datos_fecha2:
                    precio1, _, _ = fecha1_dict.get(rtr_id, (None, None, None))
                    if precio1 is not None and precio1 != precio2:
                        cambios_de_precio.append({
                            'rtr_id': rtr_id,
                            'nombre': nombre,
                            'categoria': categoria,
                            'penultimo_precio': precio1,
                            'ultimo_precio': precio2
                        })

        return render_template(
            'compare_prices.html',
            cambios_de_precio=cambios_de_precio,
            fechas_disponibles=fechas_disponibles,
            fecha1=fecha1,
            fecha2=fecha2
        )
    except Exception as e:
        return str(e), 500
    finally:
        session.close()

@app.route('/articulo/<int:rtr_id>')
def articulo_detalle(rtr_id):
    pass
















### PARTE DE JSON ###
#Todos los artículos
@app.route('/json/articulos', methods=['GET'])
def get_articulos():
    session = get_session()
    try:
        stmt = select(Articulo)
        result = session.execute(stmt)
        articulos = []
        for articulo in result.scalars():
            articulo_dict = articulo.__dict__.copy()
            articulo_dict.pop('_sa_instance_state', None)
            articulos.append(articulo_dict)
        return jsonify(articulos)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        session.close()


#Artículos por rtr_id        
@app.route('/json/articulos/<rtr_id>', methods=['GET'])
def articulos_por_id(rtr_id):
    session = get_session()
    try:
        stmt = select(Articulo).where(Articulo.rtr_id==rtr_id)
        result = session.execute(stmt)
        articulos = []
        for articulo in result.scalars():
            print(articulo)
        #     articulo_dict = articulo.__dict__.copy()
        #     articulo_dict.pop('_sa_instance_state', None)
        #     articulos.append(articulo_dict)
        # return jsonify(articulos)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        session.close()


# Artículo por categoria
@app.route('/json/categoria/<cat>', methods=['GET'])
def articulos_por_cat(cat):
    session = get_session()
    try:
        stmt = select(Articulo).where(Articulo.categoria==cat)
        result = session.execute(stmt)
        articulos = []
        for articulo in result.scalars():
            articulo_dict = articulo.__dict__.copy()
            articulo_dict.pop('_sa_instance_state', None)
            articulos.append(articulo_dict)
        return jsonify(articulos)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        session.close()
        



