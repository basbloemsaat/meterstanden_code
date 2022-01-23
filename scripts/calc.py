#!/usr/bin/env python

import json
import os
from pprint import pprint

# alle data is opgeslagen met gmt timestamps. Dit om geen data te verliezen
# rond zomer en wintertijd.
# echter voor gebruik energie wel locale tijd van belang.


def save_data_to_json(data, filename):
    filename = os.path.expanduser(filename)
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


index = {}
datapath = './docs/data/'
dailiespath = datapath + 'daily/'
# lees daily bestanden en maak index
onlyfiles = [f for f in os.listdir(dailiespath) 
    if os.path.isfile(os.path.join(dailiespath, f))]

res = map(lambda n: n[:10], onlyfiles)
index['dailies'] = list(res)

index['dailies'].sort()

pprint(index)


# wat willen we berekenen?
# gemiddelde per minuut per weekdag: 
# * 7 dagen per minuut van 00:00 tm, 23:59
# * per minuut gemiddelde, max, min



# save the index
save_data_to_json(index, datapath+'index.json')  
