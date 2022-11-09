import pickle
import numpy as np

def call_pickle(pathname):
    infile = open(pathname,'rb')
    results = pickle.load(infile)
    infile.close()
    return results

filename = 'C:/Users/Bro Soup/Desktop/University of Cambridge/Mphil in ChemE&Biotech/Heat_pump_code/pickle_files/temp_array'
gas_filename = 'C:/Users/Bro Soup/Desktop/University of Cambridge/Mphil in ChemE&Biotech/Heat_pump_code/pickle_files/gas_array'
meters_filename = 'C:/Users/Bro Soup/Desktop/University of Cambridge/Mphil in ChemE&Biotech/Heat_pump_code/pickle_files/meters_array'
elec_filename = 'C:/Users/Bro Soup/Desktop/University of Cambridge/Mphil in ChemE&Biotech/Heat_pump_code/pickle_files/elec_array'
elec_meters_filename = 'C:/Users/Bro Soup/Desktop/University of Cambridge/Mphil in ChemE&Biotech/Heat_pump_code/pickle_files/elec_meters_array'
fuel_poor_filename = 'C:/Users/Bro Soup/Desktop/University of Cambridge/Mphil in ChemE&Biotech/Heat_pump_code/pickle_files/fuel_poor'
shapes_filename = 'C:/Users/Bro Soup/Desktop/University of Cambridge/Mphil in ChemE&Biotech/Heat_pump_code/pickle_files/shapes_array'

all_results = call_pickle(filename)
gas_results = call_pickle(gas_filename)
meters_results = call_pickle(meters_filename)
elec_results = call_pickle(elec_filename)
elec_meters_results = call_pickle(elec_meters_filename)
fuel_poor_results = call_pickle(fuel_poor_filename)
shapes_results = call_pickle(shapes_filename)

#print(all_results)
'''
meters_tensor = np.zeros((20,2))
print(all_results)
'''
print(shapes_results)
for i in range(len(shapes_results)):
 print(shapes_results[i,0])