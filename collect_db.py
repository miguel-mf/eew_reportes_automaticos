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
import datetime
import math
from tinydb import TinyDB, Query
import pandas as pd
from obspy.taup import TauPyModel
from obspy.taup import * 
from obspy.geodetics import kilometer2degrees
from obspy.geodetics import locations2degrees

tiempo_espera = 60*60 # 1 hora = 3600 s
report_db = TinyDB('report_db.json')
false_db = TinyDB('false_alert_db.json')
event_check = Query()
time_file = 'tiempo_ultima_actualizacion.dat'
model = TauPyModel(model="hussen.npz")
try:
    with open(time_file, 'r') as f:
        tiempo_ultima_actualizacion = f.read()
except:
    # En caso de que el archivo no exista
    tiempo_ultima_actualizacion = 1609459200 # 01-01-2021 0:00:00 EPOCH
    with open(time_file, 'w') as f:
        f.write(tiempo_ultima_actualizacion)
        f.close()

def tiempoViaje(ev_lat,ev_lon,loc_lat,loc_lon,dep)
	dist_deg = locations2degrees(ev_lat,ev_lon,loc_lat,loc_lon)
	arrivals= model.get_travel_times(source_depth_in_km=dep, distance_in_degree=dist_deg, phase_list='p')
	if not arrivals: # Hay que revisar la fase "p" y "P", similar "s" y "S"
		arrivals= model.get_travel_times(source_depth_in_km=dep, distance_in_degree=dist_deg, phase_list='P')
		if not arrivals: # A veces, algunas prof tienen problemas, así que se prueba con un pequeño cambio
			arrivals= model.get_travel_times(source_depth_in_km=dep+1, distance_in_degree=dist_deg, phase_list='p')
			if not arrivals:
				arrivals= model.get_travel_times(source_depth_in_km=dep+1, distance_in_degree=dist_deg, phase_list='P')
	arr_p = arrivals[0]
	p_wave = arr_p.time
	arrivals= model.get_travel_times(source_depth_in_km=dep, distance_in_degree=dist_deg, phase_list='s')
	if not arrivals:
		arrivals= model.get_travel_times(source_depth_in_km=dep, distance_in_degree=dist_deg, phase_list='S')
		if not arrivals:
			arrivals= model.get_travel_times(source_depth_in_km=dep+1, distance_in_degree=dist_deg, phase_list='s')
			if not arrivals:
				arrivals= model.get_travel_times(source_depth_in_km=dep+1, distance_in_degree=dist_deg, phase_list='S')
	arr_s = arrivals[0]
	s_wave = arr_s.time
	tiempos = {"P":p_wave,"S":s_wave}
	return tiempos
	
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
		df_CSN = pd.read_csv(Catalogo_CSN, dtype=str, sep=',', engine='python')
		csn_lon = df_CSN['longitud'].astype(float).tolist()
		csn_lat = df_CSN['latitud'].astype(float).tolist()
		csn_dep = df_CSN['profundidad'].astype(float).tolist()
		df_CSN['Date'] = df_CSN['o_time'].astype(str)
		csn_date = []
		for date in df_CSN['Date']:
			aux = datetime.datetime.strptime(tiempo, '%Y-%m-%d %H:%M:%S')
			csn_date = aux.append(datetime.datetime.timestamp(aux))
		df_CSN['the_mags'] = df_CSN['the_mags'].astype(str)
		df_CSN['tipo'] = tipo.tolist()
		csn_mag = []
		dict_prioridad = {'Mww': 0, 'Mw': 1, 'W': 2, 'L': 4, 'Ml': 5, 'b': 6, 'mww': 0, 'mw': 1}
		for string in df_CSN['the_mags']:
			string = string.split()
			prioridad = 100
			for i in range(1, len(string), 2):
				prioridad_segun_mag = dict_prioridad[string[i]]
				if prioridad_segun_mag < prioridad:
					aux = float(string[i-1])
					prioridad = prioridad_segun_mag
			csn_mag.append(aux)		
		# Cruzar las dos bases de datos y actualizar bases de datos de reporte y falsa alerta
		aux = {'csn_date': csn_date, 'csn_lon': csn_lon, 'csn_lat': csn_lat, 'csn_dep': csn_dep, 'csn_mag': csn_mag}
		sismo = pd.DataFrame(data=aux)
		sismo = sismo.assign(eew_date=0)
		sismo = sismo.assign(eew_lon=0)
		sismo = sismo.assign(eew_lat=0)
		sismo = sismo.assign(eew_mag=0)
		sismo = sismo.assign(alert_time_centinela_P=0)
		sismo = sismo.assign(alert_time_centinela_S=0)
		sismo = sismo.assign(alert_time_santiago_P=0)
		sismo = sismo.assign(alert_time_santiago_S=0)
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
			eew_comp_time = modtime[i] - csn_date[evento]
			aux = tiempoViaje(lat[i],lon[i],-23.01, -69.10,csn_dep[evento])
			alert_time_centinela_P = aux.P - eew_comp_time
			alert_time_centinela_S = aux.S - eew_comp_time
			aux = tiempoViaje(lat[i],lon[i],-33.45, -70.67,csn_dep[evento])
			alert_time_santiago_P = aux.P - eew_comp_time
			alert_time_santiago_S = aux.S - eew_comp_time
			if not sismo.search(event_check.csn_date == csn_date[evento] & event_check.eew_date != 0):
				db.update({'eew_date': ev_time[i],'eew_lon': lon[i],'eew_lat': lat[i],'eew_mag': mag[i],
					  		'alert_time_centinela_P': alert_time_centinela_P, 'alert_time_centinela_S': alert_time_centinela_S
							'alert_time_santiago_P': alert_time_santiago_P, 'alert_time_santiago_S': alert_time_santiago_S
					   		'eew_comp_time': eew_comp_time,'alertado': True}, event_check.csn_date == csn_date[evento])
			else:
				aux = sismo.get(event_check.csn_date == csn_date[evento])
				loc_csn = (aux.csn_lat,aux.csn_lon)
				dist_nuevo = 111.19*locations2degrees(lat[i], lon[i], aux.eew_lat, aux.eew_lon)
				dist_anterior = 111.19*locations2degrees(lat[i], lon[i], aux.eew_lat, aux.eew_lon)
				nota_nueva = abs(mag[i]-aux.csn_mag)/2.0 + abs(ev_time[i]-aux.csn_date)/20.0 + dist_nuevo/100
				nota_anterior = abs(aux.eew_mag-aux.csn_mag)/2.0 + abs(aux.eew_date-aux.csn_date)/10.0 + dist_anterior/70.0
				if nota_nueva < nota_anterior and modtime[i] < aux.csn_date + aux.eew_comp_time:
					db.update({'rep_date': aux.eew_date,'rep_lon': aux.eew_lon,'rep_lat': aux.eew_lat,
							   'rep_mag': aux.eew_mag, 'doble_alerta': True}, event_check.csn_date == csn_date[evento])
					db.update({'eew_date': ev_time[i],'eew_lon': lon[i],'eew_lat': lat[i],'eew_mag': mag[i],
					  			'alert_time_centinela_P': alert_time_centinela_P, 'alert_time_centinela_S': alert_time_centinela_S
								'alert_time_santiago_P': alert_time_santiago_P, 'alert_time_santiago_S': alert_time_santiago_S
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
