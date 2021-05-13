import numpy as np
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature

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
        arch_fosa = '/home/sebastian/Desktop/Tesis/GMT/XY/fosa_aux.xy'
        fosa_ascii = np.loadtxt(arch_fosa)
        LonFosa = np.asarray(fosa_ascii[:,0])
        LatFosa = np.asarray(fosa_ascii[:,1])
        deltaLon = 0.02
        ax.plot(LonFosa, LatFosa, '--k', linewidth=1.0)
