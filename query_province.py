# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 19:18:49 2022

@author: Bro Soup
"""

import json
from SPARQLWrapper import SPARQLWrapper, JSON, POST
import time
from tqdm import tqdm
import numpy as np

namespace = 'http://dbpedia.org/sparql'

query='''
PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbp:  <http://dbpedia.org/property/>
PREFIX dbr:  <http://dbpedia.org/resource/>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?countryName ?area

WHERE 
{
       ?country rdf:type dbo:Country;
                rdfs:label ?countryName;
                dbo:areaTotal ?area.  
FILTER (LANG(?countryName)="en")       
}

LIMIT 10
'''

start= time.time()
#Go QUERY NOW!!!!
sparql=SPARQLWrapper(namespace)
#sparql.setMethod(POST) #try GET
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
ret = sparql.query().convert()
#I am DONE!!!
end=time.time()

#Do some treatment here...
values=ret['results']['bindings']
head=ret['head']['vars']
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
print(res_array)
usage_vals = res_array[1:,:]

print("Query finished in a time of",np.round(end-start,1),"sec.")


#print(ret)
#print(usage_vals)
#print(res_array)