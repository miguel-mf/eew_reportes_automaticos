# eew_reportes_automaticos

Codigos para hacer reportes automáticos de alerta temprana.

- Base de datos con todos los sismos alertados:
    - Incluye Hipocentro (lon,lat,prof,tiempo), Magnitud (EEW, CSN)
    - Tiempo de emisión de alerta, Tiempo de cómputo, Tiempo de alerta a varias ubicaciones (Centinela, Santiago, un par de regiones)
    - Errores: ubicacion (lon, lat, prof), magnitud, eventos duplicados.
    - Falsas alertas.
    - Estaciones utilizadas: Listado de estaciones con magnitudes asociadas.
- Script que actualiza la base de datos cada cierto tiempo (1 hora).
- Script para actualizar la base de datos manualmente para periodos de tiempo definidos por el usuario.
- Reportes automáticos para eventos con magnitud sobre 5.0 (CSN).
- Reportes automáticos mensuales.
- Reportes automáticos anuales.
- Reportes programables para periodos de tiempo, magnitud y ubicacion definidos por el usuario.




