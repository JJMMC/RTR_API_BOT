from app import app
from scripts.sqlalch_update import update_scraped
from scripts.sqlalch_consultas import delete_rows_by_date
from scripts.compare_prices import comparar_precio_ultimas_fechas, detectar_cambios_precio_en_historico
from scripts.compare_prices import get_todos_rtrids, plot_evo_precio, detectar_cambios_precio_en_historico_de_un_rtr_id
from scripts.compare_prices import get_todos_datos_por_rtrid


if __name__ == "__main__":

    app.run(debug=True)
