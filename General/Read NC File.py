import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

def read_nc(var_name,loc):
    '''
    Given a variable in the HadUK Grid dataset, reads the file
    and returns the grid of observations.
    '''
    fn = 'C:/Users/jx309/Desktop/git_project/Data/Climate Files/'+var_name+'_hadukgrid_uk_1km_mon_202001-202012.nc'
    ds = nc.Dataset(fn)
    var_grid = ds.variables[var_name][:]
    if loc == True:
        lon = ds.variables['longitude'][:]
        lat = ds.variables['latitude'][:]
        plt.contourf(lon,lat,var_grid[7,:,:])
        plt.show()
        ds.close()
        print(var_grid)
        return lon, lat, var_grid
    else:
        ds.close()
        return var_grid

lon,lat,tas = read_nc('tas',loc=True)
tasmin = read_nc('tasmin',loc=False)
tasmax = read_nc('tasmax',loc=False)


#print(tas)
'''
print(np.shape(tas))
print(np.shape(tasmin))'''