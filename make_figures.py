from plotUtil import *
import datetime
import calendar

Fecha_Inicio = '04-12-2020'  # Formato: DD-MM-YYYY (GMT)
Fecha_Termino = '11-05-2021' # Formato: DD-MM-YYYY (GMT)
lonmin = -80
lonmax = -66
latmin = -48
latmax = -16.5

# Todo Chile latmin = -48; latmax = -16.5; lonmin = -80; lonmax = -66;

db = 'report_db.json'
figura_sismo = 'figura_sismo.png'
figura_histo = 'figura_histo.png'
figura_centinela = 'figura_centinela.png'
figura_santiago = 'figura_santiago.png'

aux = datetime.datetime.strptime(Fecha_Inicio, '%d-%m-%Y')
tmin = calendar.timegm(aux.timetuple())
aux = datetime.datetime.strptime(Fecha_Termino, '%d-%m-%Y')
tmax = calendar.timegm(aux.timetuple())

#plotEarthquakeAssoc(figura_sismo,latmin,latmax,lonmin,lonmax,tmin,tmax,db)
#plotErrorHist(figura_histo,latmin,latmax,lonmin,lonmax,tmin,tmax,db)
plotTiempoAlerta(figura_centinela,figura_santiago,latmin,latmax,lonmin,lonmax,tmin,tmax,db)
