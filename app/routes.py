from app import app, db
from flask import request, jsonify, render_template
from app.models import Articulo, HistorialPrecio
from sqlalchemy import select
from scripts.dbsetup import get_session
from scripts.compare_prices import comparar_precio_ultimas_fechas


@app.route('/')
def index():
    return render_template('index.html', title="Home")


@app.route('/compare_prices')
def compare_prices():
    cambios_de_precio = comparar_precio_ultimas_fechas()
    return render_template('compare_prices.html', cambios_de_precio=cambios_de_precio)
















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
        



