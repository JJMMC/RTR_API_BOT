from sqlalchemy import insert, select, join
#from sqlalchemy.orm import sessionmaker
from app.models import Articulo, HistorialPrecio
from scripts.dbsetup import get_session
from scripts.scrap_url import scrap_rtr_crawler, scrap_rtr_crawler_by_cat
#from datetime import datetime


### FUNCIONES CONVERSION ###

# Convertimos el Return en Dict para importar en lote con SQLAlchemy
def scraped_to_dict(list_productos_tuplas):
    scraped_dict_lst = []
    for cat, rtr_id, nombre, precio, ean, art_url, img_url, fecha in list_productos_tuplas:
        producto = {
            'categoria': cat,
            'rtr_id': rtr_id,
            'nombre': nombre,
            'precio': precio,
            'ean': ean,
            'art_url': art_url,
            'img_url': img_url,
            'fecha': fecha
        }
        scraped_dict_lst.append(producto)
    return scraped_dict_lst


### FUNCIONES INSERT ###

# La primera vez que insertamos en tabla artículos
def first_insert_scaraped_articulos(list_products=None):
    list_products = scrap_rtr_crawler()
    products_dict = scraped_to_dict(list_products)
    session = get_session()
    for product in products_dict:
        # Insertar el artículo directamente
        print('Insertando artículo...')
        session.execute(insert(Articulo), [product])
    session.commit()  

# Funcion para insertar 1 FILA en TABLA ARTICULOS
def insert_articulo(product_data):
    session = get_session()
    try:
        print('Insertando artículo...')
        session.execute(insert(Articulo), [product_data])
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

#Función para insertar 1 FILA en TABLA HISTORIAL
def insert_precio(product_data):
    session = get_session()
    try:
        print('Insertando precio...')
        session.execute(insert(HistorialPrecio), [product_data])
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


# Comprobamos si el producto está ya declarado en la tabla artículos
def articulo_already_in_table(product_data):
    session = get_session()
    stmt = select(Articulo).where(Articulo.rtr_id == product_data['rtr_id'])
    result = session.execute(stmt).scalar_one_or_none()
    if result is None:
        # Si no existe, insertar el artículo
        #print('Articulo no declarado, Insertando....')
        session.close()
        return False
    else:
        session.close()
        return True

# Comprobamos si ya hay un precio para ese artículo en la fecha dada
def date_already_in_table(product_data):
    session = get_session()
    stmt = select(HistorialPrecio.fecha).where(HistorialPrecio.rtr_id == product_data['rtr_id'])
    result = session.execute(stmt).all()
    fechas_in_db = [fecha[0] for fecha in result]
    if product_data['fecha'] in fechas_in_db:
        print('Precio-Producto ya almacenado para esa fecha')
        session.close()
        return True
    else:
        session.close()
        return False


    


 


    # if product_data['fecha'] in result:
    #     print('Este artículo ya se capturó para esta fecha')
    #     session.close()
    #     return True
    # else:
    #     print('El artículo no se encuentra en la base de datos')
    #     session.close()
    #     return False

# Insertar artículos desde scrapping
def insert_scraped(list_products=None):
    products_dict = scraped_to_dict(list_products)

    for product in products_dict:
        # Comprobamos si el producto ya esta en tabla artículos
        print('Comprobando si el artículo esta declarado......')
        if articulo_already_in_table(product) == False:
            print('No está declarado.')
            insert_articulo(product)
            print('Artículo insertado')
            insert_precio(product)
            print('Precio insertado')
        else:
            print('Si está declarado.')
            print('Comprobando Fechas')
            if date_already_in_table(product) == False:
                print('Todo Correcto. Insertando precio....')
                insert_precio(product)
            else:
                print('Revisar',product,'Ya importado?')
        
# Main Update insert Funccion
def update_scraped():
    scraped_data = scrap_rtr_crawler()
    insert_scraped(scraped_data)

def update_scraped_by_cat(given_cat = 'Coches'):
    scraped_data = scrap_rtr_crawler_by_cat(given_cat)
    insert_scraped(scraped_data)





