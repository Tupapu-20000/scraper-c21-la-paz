import requests
import pandas as pd
import time
from datetime import date
def bajar_paginas(url_base):
 todas = []

 for pagina in range(1, 8):

   url = f"{url_base}/pagina_{pagina}?json=true"
   try:

    respuesta2 = requests.get(url, headers=headers, timeout=10)
    print("estado de la web:", respuesta2.status_code)

    datos_web = respuesta2.json()
    propiedades = datos_web["results"]
    todas.extend(propiedades)
    print("Encontrado", len(propiedades), datos_web["totalHits"])
   except Exception as error:
    print(f"fallo la pagina {pagina}: {error}") 
    continue

   time.sleep(1)
 return todas
urlinmobiliaria = "https://c21.com.bo/v/resultados/en-pais_bolivia/en-estado_la-paz"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
todas = bajar_paginas(urlinmobiliaria)
print("Propiedades encontradas:", len(todas))
urls = []
for p in todas:
    urls.append(p["urlCorrectaPropiedad"])

print("Total de URLs:", len(urls))
print("URLs distintas:", len(set(urls)))
def armar_filas(lista_propiedades): 
    
 filas = []
 omitidas = 0
 for p in lista_propiedades:

    m2_terreno = p.get("m2T")                                        
    if p.get("unidadDeMedida") == "ha" and m2_terreno is not None:   
        m2_terreno = round(m2_terreno * 10000, 2)
    titulo = p.get("encabezado", "").lower()
    es_anticretico = "anticr" in titulo
    es_hectarea = p.get("unidadDeMedida") == "ha"
    try:
        precio_original = float(p["precio"])
        precio_usd = p["precios"]["vista"]["precio"]
    except(KeyError, TypeError, ValueError):
        omitidas += 1
        continue

    fila = {
        "ID": p.get("id"),
        "Nombre": p.get("encabezado", "SIN NOMBRE"),
        "Fecha Publicado": p.get("fechaAlta"),
        "Fecha Modificado": p.get("fechaModificacion"),
        "Operación": p.get("tipoOperacion"),
        "Tipo": p.get("tipoPropiedadTrans"),
        "Anticrético": es_anticretico,
        "Revisar": es_hectarea,
        "Municipio": p.get("municipio"),
        "Unidad": p.get("unidadDeMedida"),
        "Zona": p.get("colonia"),
        "m2 terreno": m2_terreno,
        "m2 construcción": p.get("m2C"),
        "Estacionamiento": p.get("estacionamientos"),
        "Habitaciones": p.get("recamaras"),
        "Baños": p.get("banos"),
        "Mascotas": p.get("mascotas"),
        "Cuota Mantenimiento": p.get("cuotaMantenimiento"),
        "coordenadas latitud": p.get("lat"),
        "coordenadas longitud": p.get("lon"),
        "Afiliado": p.get("nombreAfiliado"), 
        "Moneda original": p.get("moneda"),
        "Precio original": precio_original,
        "Precio USD (sitio)": precio_usd,
        "Link": "https://c21.com.bo" + p["urlCorrectaPropiedad"],
    }

    filas.append(fila)
 print("Propiedades omitidas:", omitidas)
 return filas


filas =  armar_filas(todas)
df = pd.DataFrame(filas)
repetidas = df.duplicated(subset=["Nombre", "Precio original", "m2 construcción"], keep=False)           # NUEVO
print("filas involucradas Repetidas", repetidas.sum())
df["Posible Repetida"] = repetidas

grupo = df[repetidas]. sort_values("Nombre")
grupo.to_excel("gruporepetido.xlsx", index=False)
def Guardarexcel():
    hoy = date.today()
    nombre_archivo = f"lista_c21_{hoy}.xlsx"
    df.to_excel(nombre_archivo, index=False)
    print("Excel creado.", nombre_archivo, len(df), "filas")
    return nombre_archivo
Guardarexcel()
def mostrar_resumen(resumido):
    print("---RESUMEN GENERAL---")

    total = len (df)
    nticretico = df["Anticrético"].sum()
    Reviso = df["Revisar"].sum()
    Repeticion = df["Posible Repetida"].sum()
    ventas = (df["Operación"] == "venta").sum()
    rentas = (df["Operación"] == "renta").sum()

    print(f"{total} Propiedades - {ventas} en Venta - {rentas} en Renta - {nticretico} Anticreticos - {Reviso} Por Revisar - {Repeticion} Repetidas")

    
mostrar_resumen(df)
