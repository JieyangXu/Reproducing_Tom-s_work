# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 08:54:33 2022

@author: Bro Soup
"""
import matplotlib.patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from enum import unique
from typing import Type
from SPARQLWrapper import SPARQLWrapper, CSV, JSON, POST
from numpy.core.defchararray import add
from tqdm import tqdm 
import numpy as np 
import scipy.stats as st
import matplotlib.pyplot as plt
import geopandas as gpd
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from datetime import datetime
from geomet import wkt
import shapely.wkt
import seaborn as sb 
import json
import imageio
import rdflib
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd 
import uuid 
import time
import matplotlib.colors as cl 
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD
import pickle

def call_pickle(pathname):
    infile = open(pathname,'rb')
    results = pickle.load(infile)
    infile.close()
    return results

def save_pickle(query,pathname):
    results = query(limit=False)
    outfile = open(pathname,'wb')
    pickle.dump(results,outfile)
    outfile.close()
    return results
'''
filename = 'pickle_files/temp_array'
gas_filename = 'pickle_files/gas_array'
meters_filename = 'pickle_files/meters_array'
elec_filename = 'pickle_files/elec_array'
elec_meters_filename = 'pickle_files/elec_meters_array'
fuel_poor_filename = 'pickle_files/fuel_poor'
'''
temp_filename = 'pickle_files/temp_array'

#all_results = call_pickle(filename)
'''
gas_results = call_pickle(gas_filename)
meters_results = call_pickle(meters_filename)
elec_results = call_pickle(elec_filename)
elec_meters_results = call_pickle(elec_meters_filename)
fuel_poor_results = call_pickle(fuel_poor_filename)
'''
temp_results = call_pickle(temp_filename)

min_temp = [] 
mean_temp = [] 
max_temp = [] 
datetime_min = []
datetime_max = [] 
datetime_mean = []

'''
for i in range(len(temp_results)):
    if temp_results[i,1] == 'http://www.theworldavatar.com/kb/ontogasgrid/climate_abox/tasmin':
        min_temp.append(float(temp_results[i,-1]))
        datetime_min.append(datetime.strptime(temp_results[i,2], '%Y-%m-%dT%H:%M:%S.000Z'))
    elif temp_results[i,1] == 'http://www.theworldavatar.com/kb/ontogasgrid/climate_abox/tas':
        mean_temp.append(float(temp_results[i,-1]))
        datetime_mean.append(datetime.strptime(temp_results[i,2], '%Y-%m-%dT%H:%M:%S.000Z'))
    else:
        max_temp.append(float(temp_results[i,-1]))
        datetime_max.append(datetime.strptime(temp_results[i,2], '%Y-%m-%dT%H:%M:%S.000Z'))
        
'''

for i in range(len(temp_results)):
  if temp_results[i,1] == 'http://www.theworldavatar.com/kb/ontogasgrid/climate_abox/tasmin':
      min_temp.append(round(float(temp_results[i,-1]),1))
      datetime_min.append(datetime.strptime(temp_results[i,2], '%Y-%m-%dT%H:%M:%S.000Z'))
  elif temp_results[i,1] == 'http://www.theworldavatar.com/kb/ontogasgrid/climate_abox/tas':
      mean_temp.append(round(float(temp_results[i,-1]),1))
      datetime_mean.append(datetime.strptime(temp_results[i,2], '%Y-%m-%dT%H:%M:%S.000Z'))
  else:
      max_temp.append(round(float(temp_results[i,-1]),1))
      datetime_max.append(datetime.strptime(temp_results[i,2], '%Y-%m-%dT%H:%M:%S.000Z'))  
      
'''
Plot the temperature    
plt.figure()
plt.xlabel('Time')
plt.ylabel('C')
plt.title("LSOA")
plt.scatter(datetime_max,max_temp,label='Max Air Temperature')
plt.scatter(datetime_min,min_temp,label='Min Air Temperature')
plt.scatter(datetime_mean,mean_temp,label='Mean Air Temperature')
plt.grid()
plt.legend()
plt.show()
'''
tensor=np.zeros((3,3,3))
print(tensor)