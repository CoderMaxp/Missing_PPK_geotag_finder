# Missing_PPK_geotag_finder

**ENGLISH**

Program to find missing geotags in a post-processed GPS UAV file.

This script is compatible with .pos files generated with RTKPOST -QT ver 2.4.3 Emlid b33 or with Emlid Studio, and Emlid M+ gnss receiver(and maybe M2 receiver).

For the script to run well:
1- The images have to be taken continuously, as the calculation of missing geotags is based in the distance between consecutive images.
2-The .pos file must be in the same folder as the .py file where the code is executed from.

It may not give correct results in the case where all tags from a curve (between 2 parallel lines of the flight) are missing.

The script is written in Python and is provided 'as is', without any warranties. It may contain errors and the end user should check the data produced.

**SPANISH**

Programa para encontrar etiquetas geográficas faltantes en un archivo GPS UAV postprocesado.

Este script es compatible con archivos .pos generados con RTKPOST -QT ver 2.4.3 Emlid b33 o con Emlid Studio y el receptor Emlid M+ gnss (y tal vez el receptor M2).

Para que el script funcione bien:
1- Las imágenes deben tomarse de forma continua, ya que el cálculo de las etiquetas geográficas que faltan se basa en la distancia entre imágenes consecutivas.
2- El archivo .pos debe estar en la misma carpeta que el archivo .py desde donde se ejecuta el código.

Es posible que no proporcione resultados correctos en el caso de que falten todas las etiquetas de una curva (entre 2 líneas paralelas del vuelo).

El script está escrito en Python y se proporciona "tal cual", sin ninguna garantía. Puede contener errores y el usuario final debe comprobar los datos producidos.
