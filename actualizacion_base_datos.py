#!/usr/bin/python
import psycopg2
from config import config
import time
import math

tiempo_actualizacion = 60*60 # 1 hora = 3600 s

def connect():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    cur = conn.cursor()
    
    while True:
        #cur.execute('SELECT lon,lat,mag,time,modtime from epic.e2event where first_alert = true and modtime > %s order by modtime desc limit 1;' % (t))
        #query = cur.fetchone()
        #lon,lat,mag,ev_time,modtime = query
        time.sleep(tiempo_actualizacion)


if __name__ == '__main__':
    connect()
