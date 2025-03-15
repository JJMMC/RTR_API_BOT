from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

discipline_url = 'https://www.rtrvalladolid.es/87-crawler'

## GENERADORES ##
#Función generador de sopas
def soup_generator(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        content = res.text
        soup = BeautifulSoup(content, "html.parser")
        return soup
    except requests.RequestException as e: #Falta definir ¿qué pasa si la url no se ha scrapeado
        print(f"Error fetching {url}: {e}")
        return None


## OBTENIENDO URLS ##
# Función para obtener las CAT y CAT_URLS
def request_categorias_and_main_urls(url="https://www.rtrvalladolid.es/87-crawler"):
    soup = soup_generator(url)
    if not soup:
        return
    soup_categorias = soup.find("ul", class_="category-sub-menu").find_all("a")
    los_submenus = soup.find("ul", class_="category-sub-menu").find_all("a", class_="category-sub-link")
    soup_categorias = [url for url in soup_categorias if url not in los_submenus]
    categorias = [i.string.strip() for i in soup_categorias]
    categorias_urls = [i.get("href") for i in soup_categorias]
    for categoria, url in zip(categorias, categorias_urls):
        yield categoria, url

# Función que dada la cat_url de la categoria retorna list() de las urls (páginas) que descuelgan de ella para extraer los datos
def find_child_urls(cat_url):
    for i in range(1, 10):
        test_url = f"{cat_url}?page={str(i)}"
        soup = soup_generator(test_url)
        if not soup:
            continue
        vacio = soup.find(class_="page-content page-not-found")
        if vacio is None:
            yield test_url
        else:
            break

#######################

# Damos formato al precio para dejarlo como queremos
def formating_price(price_list):
    formated_price = []
    for i in price_list:
        precio = i.text.replace("€", "").replace(",", ".").strip()
        if len(precio) > 6:
            precio = precio.replace(".", "", 1)
        formated_price.append(precio)
    return formated_price

# Añadimos el texto que falta a los articulos con "..."
def correcion_nombre(nombre_incompleto, nombre_url):    
    nombre_incompleto = nombre_incompleto.replace('...','')    
    nombre_incompleto_lst = nombre_incompleto.replace('/','').lower().split()
    palabras_falta = ''
    
    for i in nombre_url.lower().split():
        if i in nombre_incompleto_lst:
            continue
            #print('Palabra presente')
        else:
            palabras_falta = f'{palabras_falta} {i.capitalize()}'
    
    return (nombre_incompleto + palabras_falta)
    
# Scrap info from the URL as an string
def extract_product_info_from_url(url):
    pattern = r"(-\d+[\w-]+)\.html"
    match = re.search(pattern, url)
    if match:
        full_match = match.group(1)
        #print(full_match)
        
        pattern = r"^-(\d+)"
        rtr_id_num = re.search(pattern, full_match)
        rtr_id_num = rtr_id_num.group(1)
        #print(rtr_id_num)

        pattern = r"-(\d+)$"
        ean_num = re.search(pattern, full_match)
        if ean_num:
            ean_num = ean_num.group(1)
        else:
            ean_num = None
        #print(ean_num)

        pattern = r"-\d+([a-zA-Z0-9-]+)-\d+$"
        item_name = re.search(pattern, full_match)
        if item_name:
            item_name = item_name.group(1)
        else:
            pattern = r"-\d+([a-zA-Z0-9-]+)"
            item_name = re.search(pattern, full_match)
            item_name = item_name.group(1)
        #print(item_name)
        item_name = item_name.replace("-", " ")
        item_name = item_name.capitalize()
        #print(item_name)
        return (rtr_id_num, item_name, url, ean_num)
    
    else:
        print(" OOOOOJJJJJJOOOOO no match")
        return None

# Scrapp all info from a Single Child URL
def scrap_product_details(url, cat):    
    print("\nObteniendo informacion:", url)

    # Generamos la sopa para la url child
    child_soup = soup_generator(url)

    # Obtenemos la lista de urls de cada uno de los artículos en esa Child
    prod_hrefs_lst = [href.a.get('href') for href in child_soup.find_all('div', class_='product-description')]

    # Obtenemos los nombres para poder procesarlos
    prod_name_lst = [name.string for name in child_soup.find_all('h2')]
    prod_name_from_url_lst = [extract_product_info_from_url(href)[1] for href in prod_hrefs_lst]
    prod_name_for_processing = list(zip(prod_name_lst,prod_name_from_url_lst))
 
 
 
    #Procesamos los nombres
    prod_name_final_lst = []
    for name, name_from_url in prod_name_for_processing:
        if '...' in name:
            nombre_corregido = (correcion_nombre(name,name_from_url))
            prod_name_final_lst.append(nombre_corregido)
        else:
            prod_name_final_lst.append(name)
            

    
    # Obtenemos rtr_id, y ean
    #prod_name_lst = [extract_product_info_from_url(href)[1] for href in prod_hrefs_lst]
    prod_rtr_id_art_lst = [extract_product_info_from_url(href)[0] for href in prod_hrefs_lst]
    prod_ean = [extract_product_info_from_url(href)[3] for href in prod_hrefs_lst]

    # Obtenemos el precio de cada uno de los productos
    prod_price_lst = [precio.string for precio in child_soup.find_all('span', class_='price')]
    prod_price_lst = formating_price(prod_price_lst)

    # Obtenemos la ruta de las imagenes
    prod_img_url_lst = child_soup.find_all('a', class_='thumbnail')
    prod_img_url_lst = [img_url.img.get('data-full-size-image-url') for img_url in prod_img_url_lst]

    # Genereamos una lista con la Categoria de la URL_CHILD
    prod_cat_lst = [cat] * len(prod_price_lst)

    # Generamos Fecha de obtención de datos
    fecha = datetime.now().date()
    prod_fecha_lst = [fecha] * len(prod_price_lst)

    # Asegurémonos de que todas las listas tienen el mismo número de elementos
    if not (len(prod_fecha_lst) == len(prod_cat_lst) == len(prod_rtr_id_art_lst) == len(prod_name_final_lst) == len(prod_price_lst) == len(prod_ean) == len(prod_hrefs_lst) == len(prod_img_url_lst)):
        print("Error: Las listas no tienen el mismo número de elementos")
        return []

    return list(zip(prod_cat_lst, prod_rtr_id_art_lst, prod_name_final_lst, prod_price_lst, prod_ean, prod_hrefs_lst, prod_img_url_lst, prod_fecha_lst))

# Comprobación de duplicidad de precios en el Scrapeo
def check_precios_duplicados(products_details_scraped):
    id_unicos = []
    id_duplicados = []
    final_product_details_sacraped = []

    #Localizamos los duplicados
    for product in products_details_scraped:
        cat_scr, rtr_id, name, price, ean, art_url, img_url, fecha = product
        if rtr_id not in id_unicos:
            print('No esta en la lista de comprobados')
            id_unicos.append(rtr_id)
            final_product_details_sacraped.append(product)
        else:
            print('Si esta en la lista de comprobados')
            id_duplicados.append(rtr_id)
            
    print("")
    print('Los ids UNICOS son:')
    print(id_unicos)
    print("")
    print("")
    print('Los ids DUPLICADOS son:')
    print(id_duplicados)
    print("")
    print("")
    print('Final LIST son:')
    print(len(final_product_details_sacraped))
    print("")

    return final_product_details_sacraped

# - Main - Scrap all info from all childs from all categories.
def scrap_rtr_crawler():
    product_details_scrapped = []
    for cat, cat_url in request_categorias_and_main_urls():#ojo
        print("")
        print('Scraping :', cat)
        for child_url in find_child_urls(cat_url):
            for product_details in scrap_product_details(child_url, cat):
                product_details_scrapped.append(product_details)

    return check_precios_duplicados(product_details_scrapped)

def scrap_rtr_crawler_by_cat(given_cat):
    product_details_scrapped = []
    for cat, cat_url in request_categorias_and_main_urls():
        if cat == given_cat:
            print("")
            print('Scraping :', cat)
            for child_url in find_child_urls(cat_url):
                for product_details in scrap_product_details(child_url, cat):
                    product_details_scrapped.append(product_details)

    return check_precios_duplicados(product_details_scrapped)


