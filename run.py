from app import app
from scripts.sqlalch_update import update_scraped
from scripts.sqlalch_consultas import delete_rows_by_date

if __name__ == "__main__":
    fecha_a_eliminar = '2025-03-15'  
    #delete_rows_by_date(fecha_a_eliminar)
    #update_scraped()
    app.run(debug=True)
