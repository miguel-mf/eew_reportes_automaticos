#!/usr/bin/python
"""collect_db
Se encarga de recolectar los datos de alerta temprana y mantener la
base de datos actualizada automáticamente (definido en tiempo_espera).

Algunos datos a tener en cuenta:

- Este código debería permanecer corriendo contínuamente.

- Tiene un tiempo de última actualización para partir desde ese punto
  en caso de que el proceso se llegara a parar.

- Para el funcionamiento de este código existen 3 bases de datos:
    - Base de datos psql Epic (Sismos alertados por el EEWS)
    - Base de datos CSN (Sismos reportados por CSN)
    - Base de datos TinyDB (Para ser usada en los reportes)
"""
# Preambulo
import psycopg2
from config import config
import time
import math
from tinydb import TinyDB, Query

tiempo_espera = 60*60 # 1 hora = 3600 s
report_db = TinyDB('db.json')
event_check = Query()
time_file = 'tiempo_ultima_actualizacion.dat'
try:
    with open(time_file, 'r') as f:
        tiempo_ultima_actualizacion = f.read()
except:
    # En caso de que el archivo no exista
    tiempo_ultima_actualizacion = 1609459200 # 01-01-2021 0:00:00 EPOCH
    with open(time_file, 'w') as f:
        f.write(tiempo_ultima_actualizacion)
        f.close()

def connect():
    """ Funcion que se encarga de conectarse a las bases de datos 
    y actualizar la base de datos para repores automaticos. """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    cur = conn.cursor()
    
    while True:
        # Leer base de datos PSQL/EEWS
        tiempo_ultima_actualizacion = time.time()
        cur.execute('SELECT lon,lat,mag,time,modtime from epic.e2event where first_alert = true and modtime > %s order by modtime asc;' % (tiempo_ultima_actualizacion))
        query = cur.fetchone()
        if not query:
            with open(time_file, 'w') as f:
                f.write(tiempo_ultima_actualizacion)
                f.close()
            time.sleep(tiempo_espera)
            continue
        lon,lat,mag,ev_time,modtime = query
        # Leer base de datos CSN
        
  """       # IMPORTANTE: PASAR DATE_CSN A EPOCH
            # IMPORTANTE: GENERAR DICCIONARIO CON EVENTOS
            """
        
        # Cruzar las dos bases de datos
        
        
        # Actualizar base de datos tinyDB
        for sismos in listado_sismos:
            if not db.search(event_check.date_csn == sismo.date_csn):
                report_db.insert({'date_csn':sismo.date_csn, 'magnitud':3.0,'ubicacion':'Ninguna', 'distancia':999999, 'date':message.date, 
					'username':message.from_user.id, 'username':message.from_user.first_name})
            else:
                report_db.update
        # Cambiar tiempo de ultima actualizacion y esperar para no sobrecargar la base psql
        with open(time_file, 'w') as f:
            f.write(tiempo_ultima_actualizacion)
            f.close()
        time.sleep(tiempo_espera) 
        


if __name__ == '__main__':
    connect()
