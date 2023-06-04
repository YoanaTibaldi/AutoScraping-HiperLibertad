import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup 


folder_path = "data"

categories_list = {
    'tecnologia': ['tv-y-video', 'audio', 'informatica', 'celulares-y-tablets', 'videojuegos', 'smartwatch'],
    'electrodomesticos':['climatizacion', 'pequenos-electrodomesticos', 'lavado', 'cocinas-y-hornos', 
                         'heladeras-y-freezers','hogar-y-limpieza', 'cuidado-personal-y-salud', 'termotanques-y-calefones'],
    'hogar': ['muebles-de-interior', 'cocina-y-comedor', 'bano', 'organizacion', 'iluminacion', 'dormitorio', 
              'herramientas-y-mantenimiento', 'deco'],
    'bebidas': ['aperitivos', 'cervezas', 'gaseosas', 'jugos', 'aguas', 'vinos-y-espumantes', 'isotonicas-y-espumantes',
                'bebidas-blancas-y-licores'],
    'almacen': ['aceites-y-vinagres', 'aceitunas-y-encurtidos', 'aderezos', 'arroz-y-legumbres', 'caldos-sopas-y-pure', 
                'conservas', 'desayuno-y-merienda', 'golosinas-y-chocolates', 'harinas', 'sin-tacc', 'panificados', 
                'para-preparar', 'pastas-secas-y-salsas', 'sal-pimienta-y-especias', 'snacks'],
    'lacteos': ['dulce-de-leche', 'leches', 'cremas', 'yogures', 'mantecas-y-margarinas', 'postres-y-flanes'],
    'quesos-y-fiambres': ['quesos', 'fiambres', 'salchichas'],
    'carnes': ['carne-vacuna', 'carne-de-cerdo', 'carne-de-pollo', 'embutidos', 'pescados', 'mariscos'],
    'frutas-y-verduras': ['frutas', 'verduras', 'huevos', 'legumbres-y-semillas', 'hierbas-aromaticas', 'lena-y-carbon'],
    'taeq':['almacen-taeq', 'frutas-y-verduras-taeq', 'congelados-taeq'],
    'congelados':['frutas-congeladas', 'verduras-congeladas', 'papas-congeladas', 'comidas-preparadas', 'prefritos-congelados',
                  'helados-y-postres', 'carnes-y-pollo', 'hamburguesas-y-milanesas'],
    'pastas-frescas-y-tapas': ['levaduras-y-grasas', 'fideos-y-noquis', 'pastas-rellenas', 'tpas'],
    'limpieza':['accesorios-de-limpieza', 'calzado', 'cuidado-de-la-ropa', 'desodorantes-de-ambiente', 'insecticidas', 
                'lavandina', 'limpieza-de-bano', 'limpieza-de-cocina', 'limpieza-de-pisos-y-muebles', 'papeles'],
    'perfumeria': ['cuidado-capilar', 'cuidado-oral', 'cuidado-personal', 'cuidado-de-la-piel', 'proteccion-femenina',
                   'proteccion-para-adultos', 'farmacia'],
    'bebes-y-ninos': ['higiene-y-salud', 'lactancia-y-alimentacion', 'seguridad-del-bebe', 'paseo-del-bebe', 'vehiculos-infantiles',
                      'muebles-infantiles', 'jugueteria', 'accesorios', 'panales-y-toallitas-humedas'],
    'vehiculos': ['accesorios-para-automoviles', 'accesorios-para-motos', 'neumaticos'],
    'mascotas': ['alimentos', 'accesorios-para mascotas'],
    'aire-libre-y-jardin': ['camping', 'piletas', 'cuidado-del-jardin', 'muebles-de-exterior', 'asador', 'iluminacion-exterior'],
    'libreria': ['libreria-y-papeleria'],
    'deportes': ['fitness', 'bicicletas', 'accesorios-deportivos', 'patinaje']   
}


sucursal = list(range(1, 17))
df_list = []
df_dict = {}

for categories, values in categories_list.items():
    for value in values:  
        for sc in sucursal: 
            from_ = 0
            to_ = 23
            while True:              
                json_url = f'https://www.hiperlibertad.com.ar/api/catalog_system/pub/products/search/{categories}/{value}?O=OrderByNameASC&_from={from_}&_to={to_}&ft&sc={sc}'
                response = requests.get(json_url)
                data = json.loads(response.text)
            
                if isinstance(data, list):  # Verificar si data es una lista válida
                    if not data:  # Verificar si data está vacío
                        print(f'No hay datos en: {categories}/{value} (sucursal {sc}), from {from_} to {to_}')
                        break
                    
                    if sc not in df_dict:
                        df_dict[sc] = pd.DataFrame({
                            'Fecha_de_publicacion': [],
                            'Nombre_del_producto': [],
                            'Categoria': [],
                            'Subcategoria': [],
                            'Codigo_del_producto': [],
                            'URL': [],
                            'Precio_publicado': [],
                            'Precio_regular': [],
                            'Stock': [],
                            'Descripcion': []
                        })
                    
                    df = pd.DataFrame({
                        'Fecha_de_publicacion': [item['releaseDate'] for item in data],
                        'Nombre_del_producto': [item['productName'] for item in data],
                        'Categoria': [item['categories'][0] for item in data],
                        'Subcategoria': [item['categories'][1] if len(item['categories']) > 1 else None for item in data],
                        'Codigo_del_producto': [item['productReferenceCode'] for item in data],
                        'URL': [item['link'] for item in data],
                        'Precio_publicado': [item['items'][0]['sellers'][0]['commertialOffer']['Price'] for item in data],
                        'Precio_regular': [item['items'][0]['sellers'][0]['commertialOffer']['ListPrice'] for item in data],
                        'Stock': [item['items'][0]['sellers'][0]['commertialOffer']['AvailableQuantity'] for item in data],
                        'Descripcion': [item['description'] for item in data]
                    })
                   
                    df_dict[sc] = pd.concat([df_dict[sc], df], ignore_index=True)
                   
                    to_ += 24
                    from_ += 24
                    break
                
                else:
                    print(f"Error en la respuesta para {categories}/{value} (sucursal {sc}), from {from_} to {to_}")
                    break

def limpiar_html(texto_html):
    soup = BeautifulSoup(texto_html, 'html.parser')
    texto_limpio = soup.get_text()
    return texto_limpio

# Guardar cada DataFrame en un archivo CSV separado por sucursal
for sc, df in df_dict.items():
    df['Descripcion'] = df['Descripcion'].apply(limpiar_html)
    file_path = os.path.join(folder_path, f'sucursal_{sc}.csv') 
    df.to_csv(file_path, index=False, escapechar=" ", sep="\t")

print("Los archivos CSV se han creado exitosamente.") 