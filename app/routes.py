from app import app, db
from flask import request, jsonify, render_template
from app.models import Articulo, HistorialPrecio
from sqlalchemy import select
from scripts.dbsetup import get_session

@app.route('/')
def index():
    return ''' "Base Datos RTR" '''


### PARTE DE JSON ###
#Todos los artículos
@app.route('/articulos', methods=['GET'])
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
@app.route('/articulos/<rtr_id>', methods=['GET'])
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
@app.route('/categoria/<cat>', methods=['GET'])
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
        


### PARTE DE HTML ###
@app.route('/index_web')
def index_web():
    return render_template('index.html', title="Home")

@app.route('/index_web/consulta', methods=['GET'])
def web_consulta():
    session = get_session()
    try:
        categorias = session.query(Articulo.categoria).distinct().all()
        fechas = session.query(HistorialPrecio.fecha).join(Articulo, HistorialPrecio.rtr_id == Articulo.rtr_id).distinct().all()
        categorias = [c[0] for c in categorias]
        fechas = [f[0] for f in fechas]
        
        # Formatear las fechas como día-mes-año
        fechas_formateadas = [fecha.strftime("%d-%m-%Y") for fecha in fechas]
        
        return render_template('consulta.html', categorias=categorias, fechas=fechas_formateadas, title="Consulta")
    
    except Exception as e:
        return jsonify({"error": str(e)})
    
    finally:
        session.close()

    