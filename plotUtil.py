import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from tinydb import TinyDB, where
def plotMap(ax, lonmin, lonmax, latmin, latmax, Convergencia=False, fosa=False):
    ax.set_xlim((lonmin, lonmax))
    ax.set_ylim((latmin, latmax))
    ax.set_aspect('equal')
    resolution='10m'
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', resolution, edgecolor='black',
                                                facecolor=cfeature.COLORS['land'], zorder=0))
    ax.add_feature(cfeature.NaturalEarthFeature('cultural', 'admin_0_countries', resolution,
                                                edgecolor='black', facecolor='none'))
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'lakes', resolution, edgecolor='none',
                                                facecolor=cfeature.COLORS['water']), alpha=0.5)
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', resolution,
                                                edgecolor=cfeature.COLORS['water'], facecolor='none'))
    ax.add_feature(cartopy.feature.OCEAN, facecolor='white')
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=0.8,
                      color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_left = True
    gl.ylabels_right = False
    gl.xlines = True
    gl.xlabel_style = {'size': 6.3, 'color': 'gray'}
    gl.ylabel_style = {'size': 6.3, 'color': 'gray'}
    # Convergencia:
    if Convergencia:
        Lonflecha = -72.2
        Latflecha = -22.5
        angle = 87 # angle of plate convergence respect to north
        ux = 0.05 * np.cos(np.deg2rad(90 - angle))
        vy = 0.05 * np.sin(np.deg2rad(90 - angle))
        QV1 = plt.quiver(Lonflecha, Latflecha, ux, vy, linewidths = 0.03,
                         angles ='uv', scale_units = 'width', scale = 0.5,
                         pivot = 'tail', color = 'r', transform = ccrs.PlateCarree(),
                         zorder = 3, alpha = 1.0)
        ax.text(Lonflecha + 0.3, Latflecha - 0.4, 'Convergencia \n (6.6 cm/año)',
                fontsize = 8, horizontalalignment = 'center',
                verticalalignment = 'center', transform = ccrs.PlateCarree())
    # Fosa:
    if fosa:
        arch_fosa = 'fosa_aux.xy'
        fosa_ascii = np.loadtxt(arch_fosa)
        LonFosa = np.asarray(fosa_ascii[:,0])
        LatFosa = np.asarray(fosa_ascii[:,1])
        deltaLon = 0.02
        ax.plot(LonFosa, LatFosa, '--k', linewidth=1.0)

def plotEarthquakeAssoc(filename,latmin,latmax,lonmin,lonmax,tmin,tmax,db_name):
    db = TinyDB(db_name)
    #sta_csn = np.loadtxt('EstacionesCSN.txt', usecols=[1,2,3])
    #sta_eew = np.loadtxt('EstacionesAlex.txt', usecols=[1,2,3])
    #sta_alex = np.loadtxt('EstacionesAMSA.txt', usecols=[1,2,3])
    colores = ['#3a3556','#f15918','#ffba00','#eec5d5','#b5afdb','#538a56','#85538a']
    Escala = 15
    Escala_Grafico = 1.5
    f = plt.figure(figsize=(8*Escala_Grafico,11*Escala_Grafico))
    ax = plt.axes(projection = ccrs.PlateCarree())
    plot = plotMap(ax, lonmin, lonmax, latmin, latmax, Convergencia=True, fosa=True)
    #ax.plot(sta_csn[:,0], sta_csn[:,1], 'v', color='black', markeredgecolor='k', zorder=9)
    #ax.plot(sta_eew[:,0], sta_eew[:,1], 'v', color='red', markeredgecolor='k', zorder=9)
    #ax.plot(sta_alex[:,0], sta_alex[:,1], 'v', color='yellow', markeredgecolor='k', zorder=9)
    query = db.search( (where('csn_date') > tmin) & (where('csn_date') < tmax)
                      & (where('csn_lat') > latmin) & (where('csn_lat') < latmax)
                      & (where('csn_lon') > lonmin) & (where('csn_lon') < lonmax)
                      & (where('alertado') == True))
    for item in query:
        ax.plot([item['csn_lon'],item['eew_lon']], [item['csn_lat'],item['eew_lat']], '-k')
        ax.scatter(item['csn_lon'], item['csn_lat'], s=item['csn_mag']**2*Escala,
                    color=colores[0], zorder=10, alpha=0.5, label="CSN")
        ax.scatter(item['eew_lon'], item['eew_lat'], s=item['eew_mag']**2*Escala,
                    color=colores[1], zorder=10, alpha=0.5, label="Epic")
    #lgnd = plt.legend(loc='upper right', fontsize=16, scatterpoints=1)
    #lgnd.legendHandles[0]._sizes = [4.5**2*Escala]
    #lgnd.legendHandles[1]._sizes = [4.5**2*Escala]
    plt.savefig(filename, bbox_inches='tight', dpi=200)

def plotErrorHist(filename,latmin,latmax,lonmin,lonmax,tmin,tmax,db_name):
    colores = ['#3a3556','#f15918','#ffba00','#eec5d5','#b5afdb','#538a56','#85538a']
    Escala = 15
    Escala_Grafico = 1.5

    db = TinyDB(db_name)
    query = db.search(  (where('csn_date') > tmin) & (where('csn_date') < tmax)
                      & (where('csn_lat') > latmin) & (where('csn_lat') < latmax)
                      & (where('csn_lon') > lonmin) & (where('csn_lon') < lonmax)
                      & (where('alertado') == True))
    err_dist = []
    err_dep = []
    err_mag = []
    err_otime = []
    for item in query:
        err_dist.append(item['err_dist'])
        err_dep.append(item['err_dep'])
        err_mag.append(item['err_mag'])
        err_otime.append(item['err_otime'])
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(8,8))
    hist = ax1.hist(err_mag, bins=31, histtype='bar', alpha=0.5, color=colores[0], edgecolor='black', linewidth=1)
    hist = ax2.hist(err_dist, bins=31, histtype='bar', alpha=0.5, color=colores[1], edgecolor='black', linewidth=1)
    hist = ax3.hist(err_dep, bins=31, histtype='bar', alpha=0.5, color=colores[2], edgecolor='black', linewidth=1)
    hist = ax4.hist(err_otime, bins=31, histtype='bar', alpha=0.5, color=colores[3], edgecolor='black', linewidth=1)
    ax1.set_ylabel('Frecuencia', fontsize=14)
    ax1.set_xlabel('Error Magnitud', fontsize=14)
    ax2.set_xlabel('Error Distancia [km]', fontsize=14)
    ax3.set_xlabel('Error Prof [km]', fontsize=14)
    ax4.set_xlabel('Error Tiempo origen [s]', fontsize=14)
    plt.savefig(filename, bbox_inches='tight', dpi=200)

def plotTiempoAlerta(filename1,filename2,latmin,latmax,lonmin,lonmax,tmin,tmax,db_name):
    colores = ['#3a3556','#f15918','#ffba00','#eec5d5','#b5afdb','#538a56','#85538a']
    Escala = 15
    Escala_Grafico = 1.5
    db = TinyDB(db_name)
    query = db.search(  (where('csn_date') > tmin) & (where('csn_date') < tmax)
                      & (where('csn_lat') > latmin) & (where('csn_lat') < latmax)
                      & (where('csn_lon') > lonmin) & (where('csn_lon') < lonmax)
                      & (where('alertado') == True))
    tiempo_alerta_centinela = []
    tiempo_alerta_santiago = []
    for item in query:
        tiempo_alerta_centinela.append(item['alert_time_centinela_S'])
        tiempo_alerta_santiago.append(item['alert_time_santiago_S'])
    f = plt.figure(figsize=(6*Escala_Grafico,3*Escala_Grafico))
    ax = plt.axes()
    bins = np.linspace(-60,60,13)
    hist = ax.hist(tiempo_alerta_centinela, bins=bins, histtype='bar', alpha=0.5, color=colores[0], edgecolor='black', linewidth=1)
    fig.set_ylabel('Frecuencia', fontsize=14)
    fig.set_xlabel('Tiempo Alerta (Centinela)', fontsize=14)
    plt.savefig(filename1, bbox_inches='tight', dpi=200)

    f = plt.figure(figsize=(6*Escala_Grafico,3*Escala_Grafico))
    ax = plt.axes()
    bins = np.linspace(-60,60,13)
    hist = ax.hist(tiempo_alerta_santiago, bins=bins, histtype='bar', alpha=0.5, color=colores[0], edgecolor='black', linewidth=1)
    fig.set_ylabel('Frecuencia', fontsize=14)
    fig.set_xlabel('Tiempo Alerta (Santiago)', fontsize=14)
    plt.savefig(filename2, bbox_inches='tight', dpi=200)
