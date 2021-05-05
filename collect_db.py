#!/usr/bin/python
"""collect_db
Se encarga de recolectar los datos de alerta temprana y mantener la
base de datos actualizada automáticamente (definido en tiempo_espera).

Algunos datos a tener en cuenta:

- Este código debería permanecer corriendo contínuamente.

- Tiene un tiempo de última actualización para partir desde ese punto
  en caso de que el proceso se llegara a parar.

- Para el funcionamiento de este código existen 4 bases de datos:
    - Base de datos psql Epic (Sismos alertados por el EEWS)
    - Base de datos CSN (Sismos reportados por CSN)
    - Base de datos TinyDB (Para ser usada en los reportes)
    - Base de datos con falsas alertas.
"""
# Preambulo
import psycopg2
from config import config
import time
import math
from tinydb import TinyDB, Query
import pandas as pd
from geopy import distance

tiempo_espera = 60*60 # 1 hora = 3600 s
report_db = TinyDB('report_db.json')
false_db = TinyDB('false_alert_db.json')
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

datProf, datDist, datTiempo = np.loadtxt('ProfDistTime.dat', delimiter=' ', usecols=(0,1,2), unpack=True)
		
def tiempoViaje(ev_lat,ev_lon,loc_lat,loc_lon,dep)
	#distancia = distance.distance((ev_lat,ev_lon), (loc_lat,loc_lon)).km
	#if distancia > 1000.0:
	#	return 300.0
	#aux = datDist[datProf==dep]
	#tiempo = datTiempo[aux==round(distancia*2.0, 1)/2.0]
	#return tiempo
	
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

		"""# IMPORTANTE: PASAR CSN_DATE A EPOCH
				"""

		# Cruzar las dos bases de datos y actualizar bases de datos de reporte y falsa alerta
		aux = {'csn_date': csn_date, 'csn_lon': csn_lon, 'csn_lat': csn_lat, 'csn_dep': csn_dep, 'csn_mag': csn_mag}
		sismo = pd.DataFrame(data=aux)
		sismo = sismo.assign(eew_date=0)
		sismo = sismo.assign(eew_lon=0)
		sismo = sismo.assign(eew_lat=0)
		sismo = sismo.assign(eew_mag=0)
		sismo = sismo.assign(alert_time_centinela=0)
		sismo = sismo.assign(alert_time_santiago=0)
		sismo = sismo.assign(eew_comp_time=0)
		sismo = sismo.assign(alertado=False)
		sismo = sismo.assign(doble_alerta=False)
		df = pd.DataFrame(data=d)
		desde = 0
		for i in range(0,len(ev_time)):
			# i: EEW
			# j: CSN
			EEW_date = ev_time[i]
			posibles_eventos = []
			for j in range(desde,len(csn_date)):
				CSN_date = csn_date[j]
				diferencia_tiempo = CSN_date - EEW_date
				if (abs(CSN_date - EEW_date) <= 60.0) && (modtime[i] > EEW_date):
					posibles_eventos.append(j)
					desde = j
			if not posibles_eventos: 
				false_alert_db.insert({'origin_time':ev_time[i], 'lon':lon[i], 'lat':lat[i], 'mag':mag[i], 'time':modtime[i]})
				continue
			distancia = 300.0
			evento = []
			for j in posibles_eventos
				aux = 111.0*math.sqrt((lon[i] - csn_lon[j])**2.0+(lat[i] - csn_lat[j])**2.0)
				if aux < distancia:
					evento = j
					distancia = aux
			if not evento: 
				false_alert_db.insert({'origin_time':ev_time[i], 'lon':lon[i], 'lat':lat[i], 'mag':mag[i], 'time':modtime[i]})
				continue
			false_alert_db.insert({'origin_time':ev_time[i], 'lon':lon[i], 'lat':lat[i], 'mag':mag[i], 'time':modtime[i]})
			alert_time_centinela = tiempoViaje(lat[i],lon[i],-23.01, -69.10,csn_dep[evento])
			alert_time_santiago = tiempoViaje(lat[i],lon[i],-33.45, -70.67,csn_dep[evento])
			eew_comp_time = modtime[i] - csn_date[evento]
			if not sismo.search(event_check.csn_date == csn_date[evento] & event_check.eew_date != 0):
				db.update({'eew_date': ev_time[i],'eew_lon': lon[i],'eew_lat': lat[i],'eew_mag': mag[i],
					  'alert_time_centinela': alert_time_centinela,'alert_time_santiago': alert_time_santiago,
					   'eew_comp_time': eew_comp_time,'alertado': True}, event_check.csn_date == csn_date[evento])
			else:
				aux = sismo.get(event_check.csn_date == csn_date[evento])
				loc_evento_nuevo = (lat[i], lon[i])
				loc_evento_anterior = (aux.eew_lat,aux.eew_lon)
				loc_csn = (aux.csn_lat,aux.csn_lon)
				dist_nuevo = distance.distance(loc_evento_nuevo, loc_csn).km
				dist_anterior = distance.distance(loc_evento_anterior, loc_csn).km
				nota_nueva = abs(mag[i]-aux.csn_mag)/2.0 + abs(ev_time[i]-aux.csn_date)/20.0 + dist_nuevo/100
				nota_anterior = abs(aux.eew_mag-aux.csn_mag)/2.0 + abs(aux.eew_date-aux.csn_date)/10.0 + dist_anterior/70.0
				if nota_nueva < nota_anterior and modtime[i] < aux.csn_date + aux.eew_comp_time:
					db.update({'rep_date': aux.eew_date,'rep_lon': aux.eew_lon,'rep_lat': aux.eew_lat,
							   'rep_mag': aux.eew_mag, 'doble_alerta': True}, event_check.csn_date == csn_date[evento])
					db.update({'eew_date': ev_time[i],'eew_lon': lon[i],'eew_lat': lat[i],'eew_mag': mag[i],
					  'alert_time_centinela': alert_time_centinela,'alert_time_santiago': alert_time_santiago,
					   'eew_comp_time': eew_comp_time,'alertado': True}, event_check.csn_date == csn_date[evento])
				else:
					db.update({'rep_date': ev_time[i],'rep_lon': lon[i],'rep_lat': lat[i],
							   'rep_mag': mag[i], 'doble_alerta': True}, event_check.csn_date == csn_date[evento])
			# Cambiar tiempo de ultima actualizacion y esperar para no sobrecargar la base psql
			with open(time_file, 'w') as f:
				f.write(tiempo_ultima_actualizacion)
				f.close()
			time.sleep(tiempo_espera) 
        
		

if __name__ == '__main__':
    connect()
