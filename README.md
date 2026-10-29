# Scraper C21 La Paz

Script en Python que extrae datos públicos de propiedades de Century 21 Bolivia (La Paz) y los guarda en un Excel con la fecha en que se ejecutó.

Fuente: https://c21.com.bo/v/resultados/en-pais_bolivia/en-estado_la-paz

## Qué obtiene

Para cada propiedad: precio, tipo de operación (venta o renta), tipo de propiedad, zona, m² de terreno y de construcción, habitaciones, baños y otras características. También marca los anticréticos, las posibles repetidas y las filas que conviene revisar.

## Qué genera

- `lista_c21_AAAA-MM-DD.xlsx`: todas las propiedades, con la fecha de ejecución en el nombre.
- `gruporepetido.xlsx`: las posibles repetidas, para revisarlas.

## Requisitos

Python y una terminal (VS Code o Cursor). En la terminal, instalar:

pip install requests pandas openpyxl

## Cómo ejecutarlo

python Proyecto00.py

## Uso responsable

- Solo datos públicos, sin iniciar sesión.
- Respeta lo indicado en el `robots.txt` del sitio (revisado el 29 de octubre de 2026): la ruta que usa el script está permitida.
- Hace una pausa de 1 segundo entre páginas para no saturar el servidor.
- No guarda datos personales (teléfonos, correos ni nombres de asesores).
- No debe usarse para entrenar modelos de IA: el sitio lo prohíbe.
- Los archivos Excel con datos no se publican.

## Limitaciones

- Los precios en USD de los anuncios publicados en bolivianos son una conversión que hace el propio sitio a 6,96 Bs por dólar. El valor real se acuerda con el agente.
- Las posibles repetidas solo se marcan, no se eliminan.
- El script lee hasta 7 páginas (700 propiedades). Si el sitio crece, quedarían fuera las demás.
- Si el sitio cambia su estructura, el script puede dejar de funcionar.