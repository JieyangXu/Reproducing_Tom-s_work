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
import os
import pickle

namespace = 'http://localhost:9999/blazegraph/namespace/ontogasgrid/sparql'

def standard_query(query,namespace,limit):
    if limit == False:
        limit = str(10000000000)
    limit = str(limit)
    # clearing terminal
    os.system('clear')
    LOCAL_KG_SPARQL = namespace
    # Querying using SPARQLWrapper for now
    sparql = SPARQLWrapper(LOCAL_KG_SPARQL)
    sparql.setMethod(POST) # POST query, not GET
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    print('Starting Query...')
    start = time.time()
    ret = sparql.query().convert()
    end = time.time()
    print('Finished in a time of ',np.round(end-start,3),' seconds')
    # parsing JSON into an array 
    values = ret['results']['bindings']
    head = ret['head']['vars']
    res_array = np.zeros((len(values)+1,len(head)),dtype='object')
    res_array[0,:] = head
    i = 1
    print('Parsing result of length '+str(len(res_array)))
    for row in tqdm(values):
        j = 0 
        for val in row.values():
            res_array[i,j] = val['value']
            j += 1 
        i += 1 
    usage_vals = res_array[1:,:]
    return usage_vals

# QUERYING TEMPERATURES 
def region_temp_query(limit):
    query='''
    PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX ons_t:    <http://statistics.data.gov.uk/def/statistical-geography#>
    PREFIX gsp:     <http://www.opengis.net/ont/geosparql#>
    PREFIX clim:     <http://www.theworldavatar.com/ontology/ontogasgrid/ontoclimate.owl#>
    PREFIX comp:     <http://www.theworldavatar.com/ontology/ontogasgrid/gas_network_components.owl#>
    PREFIX om:       <http://www.ontology-of-units-of-measure.org/resource/om-2/>

    SELECT ?s ?start ?end ?var ?t 
    WHERE
    {       
    ?s rdf:type ons_t:Statistical-Geography.
    ?s clim:hasClimateMeasurement ?m.
    ?m comp:hasStartUTC ?start;
        comp:hasEndUTC   ?end.
    ?m  clim:hasClimateVariable ?var.
    ?p om:hasPhenomenon ?m.
    ?p om:hasValue ?oval.
    ?oval om:hasNumericalValue ?t.
    }
    '''
    usage_vals = standard_query(query,namespace,limit=False)
    return usage_vals

# QUERYING GAS CONSUMPTION
def region_usage_query(limit):
    '''
    Querying the KG for all regions gas-usages in 2019 
    '''
    query='''
    PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX ons_t:    <http://statistics.data.gov.uk/def/statistical-geography#>
    PREFIX gsp:     <http://www.opengis.net/ont/geosparql#>
    PREFIX clim:     <http://www.theworldavatar.com/ontology/ontogasgrid/ontoclimate.owl#>
    PREFIX comp:     <http://www.theworldavatar.com/ontology/ontogasgrid/gas_network_components.owl#>
    PREFIX om:       <http://www.ontology-of-units-of-measure.org/resource/om-2/>

    SELECT ?s ?usage
    WHERE
    {       
    ?s rdf:type ons_t:Statistical-Geography;
     comp:hasUsed ?gas.
    ?energy om:hasPhenomenon ?gas;
            om:hasValue ?enval.
    ?enval om:hasNumericalValue ?usage.
    }
    '''
    usage_vals = standard_query(query,namespace,limit=False)
    return usage_vals

# QUERY ELECTRICY CONSUMPTION 
def region_elec_usage_query(limit):
    '''
    Querying the KG for all regions elec-usages in 2019 
    '''
    query='''
    PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX ons_t:    <http://statistics.data.gov.uk/def/statistical-geography#>
    PREFIX gsp:     <http://www.opengis.net/ont/geosparql#>
    PREFIX clim:     <http://www.theworldavatar.com/ontology/ontogasgrid/ontoclimate.owl#>
    PREFIX comp:     <http://www.theworldavatar.com/ontology/ontogasgrid/gas_network_components.owl#>
    PREFIX om:       <http://www.ontology-of-units-of-measure.org/resource/om-2/>

    SELECT ?s ?usage
    WHERE
    {       
    ?s rdf:type ons_t:Statistical-Geography;
     comp:hasConsumed ?elec.
    ?energy om:hasPhenomenon ?elec;
            om:hasValue ?enval.
    ?enval om:hasNumericalValue ?usage.
    }
    '''
    usage_vals = standard_query(query,namespace,limit=False)
    return usage_vals

# QUERYING GAS METERS
def region_meters_query(limit):
    '''
    Querying the KG for all regions gas meters in 2019 
    '''
    query='''
    PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX ons_t:    <http://statistics.data.gov.uk/def/statistical-geography#>
    PREFIX gsp:     <http://www.opengis.net/ont/geosparql#>
    PREFIX clim:     <http://www.theworldavatar.com/ontology/ontogasgrid/ontoclimate.owl#>
    PREFIX comp:     <http://www.theworldavatar.com/ontology/ontogasgrid/gas_network_components.owl#>
    PREFIX om:       <http://www.ontology-of-units-of-measure.org/resource/om-2/>
    PREFIX gg:       <http://www.theworldavatar.com/ontology/ontogasgrid/ontogasgrid.owl#>

    SELECT ?s ?con ?non
    WHERE
    {       
    ?s rdf:type ons_t:Statistical-Geography;
     gg:hasGasMeters ?met.
     ?met gg:hasConsumingGasMeters ?con.
     ?met gg:hasNonConsumingGasMeters ?non
    }
    '''
    usage_vals = standard_query(query,namespace,limit=False)
    return usage_vals

# QUERYING ELECTRICTY METERS
def region_elec_meters_query(limit):
    '''
    Querying the KG for all regions electricity meters in 2019 
    '''
    query='''
    PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX ons_t:    <http://statistics.data.gov.uk/def/statistical-geography#>
    PREFIX gsp:     <http://www.opengis.net/ont/geosparql#>
    PREFIX clim:     <http://www.theworldavatar.com/ontology/ontogasgrid/ontoclimate.owl#>
    PREFIX comp:     <http://www.theworldavatar.com/ontology/ontogasgrid/gas_network_components.owl#>
    PREFIX om:       <http://www.ontology-of-units-of-measure.org/resource/om-2/>
    PREFIX gg:       <http://www.theworldavatar.com/ontology/ontogasgrid/ontogasgrid.owl#>

    SELECT ?s ?con 
    WHERE
    {       
    ?s rdf:type ons_t:Statistical-Geography;
     gg:hasElecMeters ?met.
     ?met gg:hasConsumingElecMeters ?con.
    }
    '''
    usage_vals = standard_query(query,namespace,limit=False)
    return usage_vals

# QUERYING FUEL POVERTY (GET % AS AN OUTPUT HERE)
def region_fuel_pov_query(limit):
    '''
    Querying the KG for all regions fuel poverty in 2019 
    households and fuel poor households
    '''
    query='''

            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ofp:    <http://www.theworldavatar.com/ontology/ontofuelpoverty/ontofuelpoverty.owl#>
        PREFIX ofpt:   <http://www.theworldavatar.com/kb/ontofuelpoverty/abox/>
        PREFIX ons:     <http://statistics.data.gov.uk/id/statistical-geography/>
        PREFIX ons_t:    <http://statistics.data.gov.uk/def/statistical-geography#>

    SELECT ?s (xsd:float(?a)/xsd:float(?b) AS ?result) ?b 
    WHERE
    {       
    ?s rdf:type ons_t:Statistical-Geography;
        ofp:hasHouseholds ?houses.
     ?houses ofp:fuelpoorhouseholds ?a.
     ?houses ofp:numberofhouseholds ?b.
    }
    '''
    usage_vals = standard_query(query,namespace,limit=False)
    return usage_vals


# --------------------------------#
# Storing and calling queries     #
# from pickle files whilst        #
# testing                         #
# --------------------------------#

testing = True # True for pickle, False for query
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

filename = 'pickle_files/temp_array'
gas_filename = 'pickle_files/gas_array'
meters_filename = 'pickle_files/meters_array'
elec_filename = 'pickle_files/elec_array'
elec_meters_filename = 'pickle_files/elec_meters_array'
fuel_poor_filename = 'pickle_files/fuel_poor'
if testing == True: 
    all_results = call_pickle(filename)
    gas_results = call_pickle(gas_filename)
    meters_results = call_pickle(meters_filename)
    elec_results = call_pickle(elec_filename)
    elec_meters_results = call_pickle(elec_meters_filename)
    fuel_poor_results = call_pickle(fuel_poor_filename)
else:
    all_results = save_pickle(region_temp_query,filename)
    gas_results = save_pickle(region_usage_query,gas_filename)
    meters_results = save_pickle(region_meters_query,meters_filename)
    elec_results = save_pickle(region_elec_usage_query,elec_filename)
    elec_meters_results = save_pickle(region_elec_meters_query,elec_meters_filename)
    fuel_poor_results = save_pickle(region_fuel_pov_query,fuel_poor_filename)


# function to query and plot temperature values for a given LSOA
def plot_LSOA_temps(LSOA):
    query='''
    PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX ons_t:    <http://statistics.data.gov.uk/def/statistical-geography#>
    PREFIX ons:      <http://statistics.data.gov.uk/id/statistical-geography/>
    PREFIX gsp:     <http://www.opengis.net/ont/geosparql#>
    PREFIX clim:     <http://www.theworldavatar.com/ontology/ontogasgrid/ontoclimate.owl#>
    PREFIX comp:     <http://www.theworldavatar.com/ontology/ontogasgrid/gas_network_components.owl#>
    PREFIX om:       <http://www.ontology-of-units-of-measure.org/resource/om-2/>

    SELECT ?start ?end ?var ?t
    WHERE
    {       
    ons:%s clim:hasClimateMeasurement ?m.
    ?m comp:hasStartUTC ?start;
        comp:hasEndUTC   ?end.
    ?m  clim:hasClimateVariable ?var.
    ?p om:hasPhenomenon ?m.
    ?p om:hasValue ?oval.
    ?oval om:hasNumericalValue ?t.
    }
    '''%(LSOA)
    DEF_NAMESPACE = 'ontogasgrid'
    LOCAL_KG = "http://localhost:9999/blazegraph"
    LOCAL_KG_SPARQL = LOCAL_KG + '/namespace/'+DEF_NAMESPACE+'/sparql'
    # Querying using SPARQLWrapper for now
    sparql = SPARQLWrapper(LOCAL_KG_SPARQL)
    sparql.setMethod(POST) # POST query, not GET
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    print('Starting LSOA Temperature Query...')
    start = time.time()
    ret = sparql.query().convert()
    end = time.time()
    print('Finished in a time of ',np.round(end-start,3),' seconds')

    # parsing JSON into an array 
    values = ret['results']['bindings']
    head = ret['head']['vars']
    res_array = np.zeros((len(values)+1,len(head)),dtype='object')
    res_array[0,:] = head
    i = 1
    print('Parsing result of length '+str(len(res_array)))
    for row in tqdm(values):
        j = 0 
        for val in row.values():
            res_array[i,j] = val['value']
            j += 1 
        i += 1 

    results = res_array[1:,:]

    min_temp = [] 
    mean_temp = [] 
    max_temp = [] 
    datetime_min = []
    datetime_max = [] 
    datetime_mean = []
    for i in range(len(results)):
        if results[i,0] == 'http://www.theworldavatar.com/kb/ontogasgrid/climate_abox/tasmin':
            min_temp.append(float(results[i,-1]))
            datetime_min.append(datetime.strptime(results[i,1], '%Y-%m-%dT%H:%M:%S.000Z'))
        elif results[i,0] == 'http://www.theworldavatar.com/kb/ontogasgrid/climate_abox/tas':
            mean_temp.append(float(results[i,-1]))
            datetime_mean.append(datetime.strptime(results[i,1], '%Y-%m-%dT%H:%M:%S.000Z'))
        else:
            max_temp.append(float(results[i,-1]))
            datetime_max.append(datetime.strptime(results[i,1], '%Y-%m-%dT%H:%M:%S.000Z'))

    plt.figure()
    plt.xlabel('Time')
    plt.ylabel('C')
    plt.title(LSOA)
    plt.scatter(datetime_max,max_temp,label='Max Air Temperature')
    plt.scatter(datetime_min,min_temp,label='Min Air Temperature')
    plt.scatter(datetime_mean,mean_temp,label='Mean Air Temperature')
    plt.grid()
    plt.legend()
    plt.show()
    return 
#plot_LSOA_temps('S01011468')


unique_LSOA = np.unique(all_results[:,0]) # Get unique LSOA keys
# pre-allocated memory for temperature values (TYPE,LSOA,MONTH)
# where type is [min,mean,max]
results_tensor = np.zeros((3,len(unique_LSOA),12)) 
# preallocate yearly gas consumption per LSOA array (LSOA)
gas_tensor = np.zeros(len(unique_LSOA))
# preallocate consuming and non-consuming meters tensor (LSOA,METER)
meters_tensor = np.zeros((len(unique_LSOA),2))

elec_tensor = np.zeros(len(unique_LSOA))
# preallocate consuming and non-consuming meters tensor (LSOA,METER)
elec_meters_tensor = np.zeros(len(unique_LSOA))

fuel_poor_tensor = np.zeros(len(unique_LSOA))

households_tensor = np.zeros(len(unique_LSOA))


# Note: Using dictionaries to go from IRIs to arrays is wicked quick and better than doing nested loops

# Dictionary to convert climate var type to index in tensor
t_dict = {'http://www.theworldavatar.com/kb/ontogasgrid/climate_abox/tasmin':0,\
          'http://www.theworldavatar.com/kb/ontogasgrid/climate_abox/tas':1,\
          'http://www.theworldavatar.com/kb/ontogasgrid/climate_abox/tasmax':2}

# Dictionary to convert datetime (month) to index in tensor
date_dict = {'2019-01-01T12:00:00.000Z':0,\
             '2019-02-01T12:00:00.000Z':1,\
             '2019-03-01T12:00:00.000Z':2,\
             '2019-04-01T12:00:00.000Z':3,\
             '2019-05-01T12:00:00.000Z':4,\
             '2019-06-01T12:00:00.000Z':5,\
             '2019-07-01T12:00:00.000Z':6,\
             '2019-08-01T12:00:00.000Z':7,\
             '2019-09-01T12:00:00.000Z':8,\
             '2019-10-01T12:00:00.000Z':9,\
             '2019-11-01T12:00:00.000Z':10,\
             '2019-12-01T12:00:00.000Z':11}

# Dictionary to convert LSOA IRIs to index in tensor
lsoa_dict = {}
for i in range(len(unique_LSOA)):
    lsoa_dict[unique_LSOA[i]] = i 


# Now we have everything in place to format results into tensors 
print('Formatting query results...')

# PARSING TEMPERATURE INTO TENSOR 
# --------------------------------#
# iterating over the list of all temperature values 
for j in tqdm(range(len(all_results[:,0]))):
    # getting the right indexes based off date, temp type and LSOA key
    # (think of it as identifying the right spot in the cube)
    t_ind = t_dict[all_results[j,1]]
    d_ind = date_dict[all_results[j,2]]
    lsoa_ind = lsoa_dict[all_results[j,0]]
    # allocating a value (last index is value)
    results_tensor[t_ind,lsoa_ind,d_ind] = all_results[j,-1]

# PARSING GAS INTO TENSOR 
# --------------------------------#
# iterating over gas results query
for j in tqdm(range(len(gas_results[:,0]))):
    try:
        # try and find the index for the LSOA of each gas value
        gas_lsoa_ind = lsoa_dict[gas_results[j,0]]
        gas_tensor[gas_lsoa_ind] = gas_results[j,1]
    except KeyError: # if it doesn't exist...
        print('No gas data for ',gas_results[j,0].split('/')[-1])


# PARSING METERS INTO TENSOR
# --------------------------------#
# iterating over meters results query
for j in tqdm(range(len(meters_results[:,0]))):
    # try to identify LSOA key
    try:
        gas_lsoa_ind = lsoa_dict[meters_results[j,0]]
        meters_tensor[gas_lsoa_ind,0] = meters_results[j,1]
    except KeyError:
        print('No gas meter data for ',meters_results[j,0].split('/')[-1])
    # first is consuming gas meters
    # second is non-consuming 
    if meters_results[j,2] != '-':
        meters_tensor[gas_lsoa_ind,1] = meters_results[j,2]
    else: # if none then set to 0 (stored weirdly in KG [Sorry!])
        meters_tensor[gas_lsoa_ind,1] = 0 


# PARSING ELECTRICITY INTO TENSOR 
# --------------------------------#
# iterating over gas results query
for j in tqdm(range(len(elec_results[:,0]))):
    try:
        # try and find the index for the LSOA of each gas value
        gas_lsoa_ind = lsoa_dict[elec_results[j,0]]
        elec_tensor[gas_lsoa_ind] = elec_results[j,1]
    except KeyError: # if it doesn't exist...
        print('No electricity data for ',elec_results[j,0].split('/')[-1])


# PARSING ELECTRICITY METERS INTO TENSOR
# --------------------------------#
# iterating over meters results query
for j in tqdm(range(len(elec_meters_results[:,0]))):
    # try to identify LSOA key
    try:
        elec_lsoa_ind = lsoa_dict[elec_meters_results[j,0]]
        elec_meters_tensor[elec_lsoa_ind] = elec_meters_results[j,1]
    except KeyError:
        print('No electricity meter data for ',elec_meters_results[j,0].split('/')[-1])
    

# PARSING FUEL POVERTY INTO TENSOR
# --------------------------------#
# iterating over poverty results query
for j in tqdm(range(len(fuel_poor_results[:,0]))):
    # try to identify LSOA key
    try:
        fuel_poor_lsoa_ind = lsoa_dict[fuel_poor_results[j,0]]
        fuel_poor_tensor[fuel_poor_lsoa_ind] = float(fuel_poor_results[j,2])
    except KeyError:
        print('No fuel poverty data for ',fuel_poor_results[j,0].split('/')[-1])
    
    

# PARSING HOUSEHOLDS INTO TENSOR
# --------------------------------#
# iterating over poverty results query
for j in tqdm(range(len(fuel_poor_results[:,0]))):
    # try to identify LSOA key
    try:
        fuel_poor_lsoa_ind = lsoa_dict[fuel_poor_results[j,0]]
        households_tensor[fuel_poor_lsoa_ind] = float(fuel_poor_results[j,1])
    except KeyError:
        print('No household data for ',fuel_poor_results[j,0].split('/')[-1])
    
    


from calculation_parameters.cop_equation import COP


# vector of TOTAL gas consumption in 2019 by month
# used to scale yearly LSOA values
# ASSUMPTION: all LSOAs scale proportionately to yearly demand.
monthly_total_gas_demand = [9.7358,7.389,7.17968,8.073659,5.4084,4.4428,3.93779,3.3926,4.004,6.117,7.989,8.154]
total_uk_demand = sum(monthly_total_gas_demand)
months = ['January','February','March','April','May','June','July','August','September','October','November','December']
plot = False 
if plot == True:
    plt.figure()
    plt.grid()
    plt.title('Monthly UK gas demand')
    plt.ylabel('Billion cubic meters')
    plt.plot(np.arange(len(monthly_total_gas_demand)),monthly_total_gas_demand)
    plt.xticks(np.arange(len(months)),months)
    plt.show()
else:
    print('Not plotting temperature')

# preallocating disaggregated monthly gas consumption tensor
monthly_gas_tensor = np.zeros((len(unique_LSOA),12))

from calculation_parameters.gas_params import alpha,nb
# scaling yearly gas values for each LSOA to monthly values
for i in range(len(gas_tensor)):
    for j in range(len(months)):
        monthly_gas_tensor[i,j] = gas_tensor[i] * monthly_total_gas_demand[j] / total_uk_demand


# vector of TOTAL electricity consumption in 2019 by month
# used to scale yearly LSOA values
# ASSUMPTION: all LSOAs scale proportionately to yearly demand.
monthly_total_elec_demand = [29.61,25.1,26.13,24.67,23.75,22.3,23.19,23.01,22.82,25.75,27.48,27.82]
total_uk_elec_demand = sum(monthly_total_elec_demand)
if plot == True:
    plt.figure()
    plt.grid()
    plt.title('Monthly UK electricity demand')
    plt.ylabel('Terrawatt Hours')
    plt.plot(np.arange(len(monthly_total_elec_demand)),monthly_total_elec_demand)
    plt.xticks(np.arange(len(months)),months)
    plt.show()
else:
    print('Not plotting temperature')

# preallocating disaggregated monthly gas consumption tensor
monthly_elec_tensor = np.zeros((len(unique_LSOA),12))

# scaling yearly gas values for each LSOA to monthly values
for i in range(len(elec_tensor)):
    for j in range(len(months)):
        monthly_elec_tensor[i,j] = elec_tensor[i] * monthly_total_elec_demand[j] / total_uk_elec_demand

# Querying Polygons from KG to construct geoJSON
def query_poly(limit):
    '''
    Querying the KG for all regions gas-usages in 2019 
    '''
    if limit == False:
        limit = str(100000000)
    limit = str(limit)
    # clearing terminal
    os.system('clear')
    

    query='''
    PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX ons_t:    <http://statistics.data.gov.uk/def/statistical-geography#>
    PREFIX gsp:     <http://www.opengis.net/ont/geosparql#>

    SELECT ?s ?geom
    WHERE
    {       
    ?s rdf:type ons_t:Statistical-Geography.
    OPTIONAL{ ?s gsp:hasGeometry ?o.
            ?o gsp:asWKT ?geom}
    }
    '''
    DEF_NAMESPACE = 'ontogasgrid'
    LOCAL_KG = "http://localhost:9999/blazegraph"
    LOCAL_KG_SPARQL = LOCAL_KG + '/namespace/'+DEF_NAMESPACE+'/sparql'

    sparql = SPARQLWrapper(LOCAL_KG_SPARQL)
    sparql.setMethod(POST) # POST query, not GET
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    print('Starting Gas Usage Query...')
    start = time.time()
    ret = sparql.query().convert()
    end = time.time()
    print('Finished in a time of ',np.round(end-start,3),' seconds')

    # parsing JSON into an array 
    values = ret['results']['bindings']
    head = ret['head']['vars']
    res_array = np.zeros((len(values)+1,len(head)),dtype='object')
    res_array[0,:] = head
    i = 1
    for row in values:
        j = 0 
        for val in row.values():
            res_array[i,j] = val['value']
            j += 1 
        i += 1 

    LSOA_shapes = res_array[1:,:]

    return LSOA_shapes



def return_geo_df(month,uptake,temp_var_type):
    month_str = months[month]
    # getting mean min or max tensor
    temp_tensor = results_tensor[t_dict[temp_var_type],:,:] 
    # calculating COP
    cop_tensor = np.array(list(map(COP, temp_tensor)))      
    # caluclating converted gas to electricity via HP
    hp_in_tensor = np.divide((uptake*monthly_gas_tensor),cop_tensor) * alpha * nb 
    # calculating leftover gas 
    resulting_gas_tensor = (alpha * monthly_gas_tensor  * (1-uptake)) + ((1-alpha)*monthly_gas_tensor)
    # calculating resulting electricity 
    resulting_elec_tensor = monthly_elec_tensor + hp_in_tensor



    # importing pickle file if testing but querying from KG if not 
    shapes_filename = 'pickle_files/shapes_array'
    if testing == True:
        LSOA_shapes = call_pickle(shapes_filename)
    else:
        LSOA_shapes = save_pickle(query_poly,shapes_filename)

    # check if WKT is valid and 
    # uploading polygons to Shapely to reduce precision to 5 DP (1m)
    for i in range(len(LSOA_shapes[:,1])):
        shape = LSOA_shapes[i,1]
        try:
            P = shapely.wkt.loads(shape)
            LSOA_shapes[i,1] = shapely.wkt.dumps(P,rounding_precision=5)
        # if shape is invalid do chuff all 
        except TypeError:
            nothing = 0 
        # if the shape is just a number (basically meaningless)
        # add to index of shapes to be deleted
        if type(LSOA_shapes[i,1]) == int:
            del_ind = i 

    # get rid of invalid shapes
    LSOA_shapes = np.delete(LSOA_shapes,del_ind,axis=0)

    # convert to a dictionary
    LSOA_shapes = dict(LSOA_shapes)

    # Create arrays to extract values from the tensors from 
    # Note the tensors were just to organise everything and make 
    # sure the values are in the right place

    # preallocating memory 
    gas_values            = np.zeros((len(hp_in_tensor[:,1]),12))
    elec_values           = np.zeros_like(gas_values)
    remaining_elec_values = np.zeros_like(gas_values)
    remaining_gas_values  = np.zeros_like(gas_values)
    temp_values           = np.zeros_like(gas_values)
    delta_elec_values     = np.zeros_like(gas_values)
    delta_gas_values      = np.zeros_like(gas_values)
    shapes_of_interest    = np.zeros(len(hp_in_tensor[:,1]),dtype='object')
    cop_values            = np.zeros_like(gas_values,dtype='object')



    elec_co = 0.233
    gas_co = 0.184

    elec_per_kwh = 594 / 3600
    gas_per_kwh  = 514 / 13600

    # https://bulb.co.uk/carbon-tracker/
    # going over all the gas values
    for i in range(len(gas_values)):
        key = unique_LSOA[i] # getting the key for the specific LSOA
        # finding the respective 'shape'
        shapes_of_interest[i] = LSOA_shapes[key]
        # assigning gas consumption 
        gas_values[i,:] = monthly_gas_tensor[i,:]

        # assigning elec consumption 
        elec_values[i,:] = monthly_elec_tensor[i,:]
        # assigning temperature value
        temp_values[i,:] = temp_tensor[i,:]
        # assigning additional electricity
        delta_elec_values[i,:] = hp_in_tensor[i,:]
        # assigning COP
        cop_values[i,:] = cop_tensor[i,:]
        # assigning remaining gas values
        remaining_gas_values[i,:] = resulting_gas_tensor[i,:]

        delta_gas_values[i,:] = remaining_gas_values[i,:] - gas_values[i,:]
        # assigning remaining elec values
        remaining_elec_values[i,:] = elec_values[i,:] + delta_elec_values[i,:]

    peak_power_values = np.zeros(len(hp_in_tensor[:,1]))
    for i in range(len(gas_values)):
        peak_power_values[i] = max(remaining_elec_values[i,:])



    ## CODE FOR PLOTTING *IN* PYTHON


    df = pd.DataFrame(unique_LSOA)
    df['geometry'] = gpd.GeoSeries.from_wkt(shapes_of_interest)
    df['geom_str'] = list([str(x) for x in shapes_of_interest])
    df['Peak Power']    = list(peak_power_values)

    
    # specifying geodata frame

    my_geo_df = gpd.GeoDataFrame(df, geometry='geometry')
    my_geo_df = my_geo_df.set_crs("EPSG:4326")
    print('Converting to Mercator projection (better than WGS84 for UK)')
    my_geo_df = my_geo_df.to_crs("EPSG:3395")

    return my_geo_df

# define min mean or max 
temp_var_type = 'http://www.theworldavatar.com/kb/ontogasgrid/climate_abox/tas'


print('Change of projection completed!')
#plt.rc('text', usetex=True)
plt.rc('font', family='sans-serif')
import os
from matplotlib.colors import ListedColormap
from matplotlib import cm

top = cm.get_cmap('coolwarm', 128)

newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       np.flip(top(np.linspace(0, 1, 128)),axis=0)))

newcmp = ListedColormap(newcolors, name='ineq')

vars      = ['Peak Power']
var_names = ['Peak Power']

def plot_variables(vars,var_names,inset,month,uptake,temp_var_type):
    print('Beginning plot...')
    color_theme = 'coolwarm'

    # ADD UP EMISSIONS HERE 
    mosaic = '''
        ABCDE
        ABCDE
        '''
    fig = plt.figure(figsize=(11,5))
    axs = fig.subplot_mosaic(mosaic)    
    UK_gdf = gpd.read_file("GB_shapefile/GBR_adm2.shp")
    UK_gdf = UK_gdf.to_crs("EPSG:3395")
    uptakes = [0,0.25,0.5,0.75,1]
    my_geo_df = return_geo_df(1,1,temp_var_type)
    plot_names = ['A','B','C','D','E']
    val_values = my_geo_df[vars[0]].values
    iqr = st.iqr(val_values)
    q1,q3 = st.mstats.idealfourths(val_values)
    bottom  = q1-1.5*iqr
    top     = q3+1.5*iqr
    divnorm = cl.Normalize(vmin=bottom, vmax=top)
    for it in range(len(uptakes)):
        uptake = uptakes[it]
        axs[plot_names[it]].set_title(str(int(uptake*100))+'% Uptake',loc='left')
        my_geo_df = return_geo_df(month,uptake,temp_var_type)
        UK_gdf.boundary.plot(ax=axs[plot_names[it]],color='k',linewidth=0.5)
        boundary = my_geo_df.bounds
        boundary = [min(boundary.values[:,0]),min(boundary.values[:,1]),max(boundary.values[:,2]),max(boundary.values[:,3])]
        axs[plot_names[it]].set_ylim([boundary[1]-5E4,boundary[3]+5E4])
        axs[plot_names[it]].set_xlim(([boundary[0]-5E4,boundary[2]]))

        plt.subplots_adjust(left=0.075,right=0.836)
        if plot_names[it] == 'E':
            cax = fig.add_axes([0.9, 0.1, 0.02, 0.8])
            tl  = my_geo_df.plot(column=vars[0],cmap=color_theme,\
                antialiased=False,\
                ax = axs[plot_names[it]],\
                legend=True,\
                norm = divnorm,\
                cax=cax,
                legend_kwds={'label':'Monthly Electrical Power Consumption (kWh/month)'})  
            cax.ticklabel_format(axis="y", style="sci", scilimits=(0,0))   
        else:
            tl  = my_geo_df.plot(column=vars[0],cmap=color_theme,\
                antialiased=False,\
                ax = axs[plot_names[it]],\
                norm = divnorm)

        axs[plot_names[it]].set_xticks([])
        axs[plot_names[it]].set_yticks([])
        axs[plot_names[it]].spines["top"].set_visible(False)
        axs[plot_names[it]].spines["right"].set_visible(False)
        axs[plot_names[it]].spines["left"].set_visible(False)
        axs[plot_names[it]].spines["bottom"].set_visible(False)

    plt.savefig('figure_output/a_'+str(alpha)+'n_'+str(nb)+'/peak_power_nationwide.png',dpi=200) 
    plt.savefig('figure_output/a_'+str(alpha)+'n_'+str(nb)+'/peak_power_nationwide.pdf') 

    

    
    return 
    
inset = False
plot_variables(vars,var_names,inset,7,1,temp_var_type)
