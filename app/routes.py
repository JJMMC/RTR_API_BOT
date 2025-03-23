from app import app, db
from flask import request, jsonify, render_template
from app.models import Articulo, HistorialPrecio
from sqlalchemy import select
from scripts.dbsetup import get_session
from scripts.compare_prices import comparar_precio_ultimas_fechas, get_todos_datos_por_fecha, get_todas_fechas_distintas
from scripts.compare_prices import comparar_precio_dos_fechas
# import matplotlib.pyplot as plt
# import io
# import base64


@app.route('/')
def index():
    return render_template('index.html', title="Home")


@app.route('/compare_last_prices')
def compare_last_prices():
    cambios_de_precio = comparar_precio_ultimas_fechas()
    return render_template('compare_last_prices.html', cambios_de_precio=cambios_de_precio)

@app.route('/compare_prices', methods=['GET', 'POST'])
def compare_prices():
    fechas_disponibles = get_todas_fechas_distintas()

    fecha1 = None
    fecha2 = None
    cambios_de_precio = []

    if request.method == 'POST':
        # Obtener las fechas seleccionadas por el usuario
        fecha1 = request.form.get('fecha1')
        fecha2 = request.form.get('fecha2')

        if fecha1 and fecha2:
            cambios_de_precio = comparar_precio_dos_fechas(fecha1,fecha2)

    return render_template(
        'compare_prices.html',
        cambios_de_precio=cambios_de_precio,
        fechas_disponibles=fechas_disponibles,
        fecha1=fecha1,
        fecha2=fecha2
        )


@app.route('/articulo/<int:rtr_id>')
def articulo_detalle(rtr_id):
    session = get_session()
    try:
        stmt = select(Articulo).where(Articulo.rtr_id == rtr_id)
        articulo = session.execute(stmt).scalar_one_or_none()
        
        if articulo is None:
            return "Artículo no encontrado", 404
        
        return render_template('articulo.html', articulo=articulo)
    except Exception as e:
        return str(e), 500
    finally:
        session.close()















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
        



