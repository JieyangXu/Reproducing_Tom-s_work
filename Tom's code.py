# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 00:18:52 2022

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

namespace = 'http://localhost:9999/blazegraph/namespace/ontogasgrid/sparql'

def standard_query(query,namespace,limit):
    if limit == False:
        limit = str(10000000000)
    limit = str(limit)
    # clearing terminal
    # os.system('clear')
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
limit=False
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
print(usage_vals)