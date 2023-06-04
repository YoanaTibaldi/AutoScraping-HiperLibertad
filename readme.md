# Web Scraping a Hiper Libertad

El desafio propuesto fue desarrollar un web scraper para la pagina del hiperlibertad para recolescta todos los productos con sus precios de lista, disponibilidad, categorías, entre otros, para cada una de las sucursales, para posteriormente almacenarlos en archivos CSV individuales (uno por sucursal).
#
Requerimientos: 
- request
- pandas
- beautifulsoup4

Instalación/ Ejecución del proyecto:
- Instalar python3 
- Clonar el repositorio
- Ejecutar en consola "python data-scraping.py"

#
Se utilizará la librería request ya que en el código fuente del sitio no existe ningún producto sino que se realiza una carga asincrónica de los datos

<sup></sup>  

_La siguiente documentación explica el proceso realizado hasta obtener los resultados_

#
<sup></sup>  
1. Primero creamos un entorno virtual e instalamos las librerias que vamos a usar durante el proceso:

```
pip install request

pip install pandas

pip install beautifulsoup4
```

## Ahora manos a la obra!
<sup></sup>  

2. Importamos las librerias instaladas

```
import os

import requests

import json

import pandas as pd

from bs4 import BeautifulSoup
```

- En este caso debemos recolectar datos del siguiente sitio: "https://www.hiperlibertad.com.ar/"
<sup></sup>  
<sup></sup>  

3. Localizamos la api por medio del inspector y comenzamos a observar los parámetros que podemos utilizar para recolectar los datos. Tambien estudiamos bien el sitio web para prestar atención a las sucursales, cantidad de páginas y de productos por cada una de estas.

- Construimos un diccionario, donde sus claves son las categorias y los valores las subcategorías.
<sup></sup>  
<sup></sup>  

4. Ya teniendo todo esto podemos alterar nuestra api de la siguiente manera: f"https://www.hiperlibertad.com.ar/api/catalog_system/pub/products/search/{categories}/{value}?O=OrderByNameASC&_from={from_}&_to={to_}&ft&sc={sc}"
<sup></sup>  
<sup></sup>  

5. Para poder recorrer cada uno de los productos, pasando por categorías, páginas y sucursales creamos un _bucle for_ y comenzamos a llamar a la api utilizando la librería request:

```
**for** categories, values in categories_list.items():
    **for** value in values:  
        **for** sc in sucursal: 
            from_ = 0
            to_ = 23
            **while True**:              
                json_url = f'https://www.hiperlibertad.com.ar/api/catalog_system/pub/products/search/{categories}/{value}?O=OrderByNameASC&_from={from_}&_to={to_}&ft&sc={sc}'
                response = requests.get(json_url)
                data = json.loads(response.text)
```


_Esto se integrará dentro de un ciclo while ya que queremos saber si por cada página en la que nos dirige nuestra api hay datos, es decir, productos cargados. Por lo que creamos condicionales._


```

if isinstance(data, list) #verificamos si data es una lista válida, es decir si hay datos
    if not data: # si no hay datos, rompemos el ciclo
    if sc not in df_dict: # se asegura que "sc" no este en el diccionario y se crea una nueva entrada en el diccionario donde el valor es un DataFrame vacío con columnas predefinidas. Finalmente se actualizan los valores from_, to_ y rompemos el ciclo.
else #si data no es una lista valida, muestra un mensaje de error y rompe el ciclo

```
- Para saber si hay un error en la respuesta de alguna sucursal o categoria, se imprime un mensaje por consola para: 
    - Error en respuesta: Creado para cuando no hay respuesta por el lado de la api.
    - No hay datos: Creado para cuando la categoría está vacía.

<sup></sup>  
<sup></sup>  
6. Para crear un archivo csv por cada sucursal creamos un _ciclo for_ que tome la variable para el número de sucursal generando un archivo CSV distinto para cada clave "sc" del diccionario "df_dict" y lo almacene en la carpeta creada _"file_path"_

_Nota: Lo que hacemos con BeautifulSoup es limpiar el texto que devuelve el item "Descripcion" de json ya que al recolectarlo contenía tags perteneciente a un formato html_ 
