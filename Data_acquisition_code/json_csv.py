#!/usr/bin/env python
 # -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth
import json
import os
import glob
from pandas.io.json import json_normalize
import ast
import pandas as pd

'''

This program flattens json files collected from the DSMZ bacdive API and outputs each csv file and a combined csv file (tab delimited)  

'''


inpath='/Users/cameronmartino/bin/bacdive/'
otupath='/Users/cameronmartino/bin/bacdive/'

def flatten_json(y):
    out = {}
    for n_1,i_1 in y.items():
        for i_1point5 in i_1:
            if isinstance(i_1point5, unicode):
                for n in i_1[i_1point5]:
                    for r,i in n.items():
                        if isinstance(i, unicode):
                            i=i.encode('utf-8')
                        else:
                            i=str(i)
                        if isinstance(r, unicode):
                            r=r.encode('utf-8')
                        else:
                            r=str(r)
                        if isinstance(i_1point5, unicode):
                            i_1point5=i_1point5.encode('utf-8')
                        else:
                            i_1point5=str(i_1point5)
                        if isinstance(n_1, unicode):
                            n_1=n_1.encode('utf-8')
                        else:
                            n_1=str(n_1)
                        
                        out[n_1+"_"+i_1point5+"_"+r]=i



    return out



json_list=glob.glob("%s*.json"%inpath)
q=0

for json_tmp in json_list:
    print(json_tmp)
    #import data
    if q==0:
        objects = json.load(open(json_tmp))
        #flatten data
        flat = flatten_json(objects)
        tmp_dffjson_start=pd.DataFrame(flat.items())
        tmp_dffjson_start = tmp_dffjson_start.set_index([0])
        tmp_dffjson_start.to_csv('%s%s_json_database.csv'%(otupath,str(q)),sep="\t")
    if q>=1:
        objects = json.load(open(json_tmp))
        #flatten data
        flat = flatten_json(objects)
        tmp_dffjson=pd.DataFrame(flat.items())
        tmp_dffjson = tmp_dffjson.set_index([0])
        tmp_dffjson.to_csv('%s%s_json_database.csv'%(otupath,str(q)),sep="\t")
        tmp_dffjson_start = pd.concat([tmp_dffjson_start, tmp_dffjson], axis=1)

    q+=1

tmp_dffjson_start.to_csv('%sjson_database_all.csv'%otupath,sep="\t")





