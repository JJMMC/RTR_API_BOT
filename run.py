from app import app
from scripts.sqlalch_update import update_scraped
from scripts.sqlalch_consultas import delete_rows_by_date
from scripts.compare_prices import comparar_precio_fechas, get_precios_por_fecha

if __name__ == "__main__":
    #fecha_a_eliminar = '2025-03-15'  
    #delete_rows_by_date(fecha_a_eliminar)
    #update_scraped()
    #get_precios_por_fecha()
    #comparar_precio_fechas()



    app.run(debug=True)
