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
import wanrings

'''
This program matches the bacterial species in the distance matrix to the phenotype data collected from Bacdive
'''


inpath='/Users/cameronmartino/bin/databases_by_me/phenodata/'
otupath='/Users/cameronmartino/bin/databases_by_me/phenodata/'

def match(phylo_match, pheno_match):

    subphylo_matchids = set(phylo_match.index)
    subpheno_matchids = set(pheno_match.index)
    if len(subphylo_matchids) != len(phylo_match.index):
        raise ValueError("`phylo_match` has duplicate sample ids.")
    if len(subpheno_matchids) != len(pheno_match.index):
        raise ValueError("`pheno_match` has duplicate sample ids.")
    
    idx = subphylo_matchids & subpheno_matchids
    subphylo_match = phylo_match.loc[idx]
    subpheno_match = pheno_match.loc[idx]
    return subphylo_match, subpheno_match

pheno = pd.read_table('%sjson_database_all.csv'%inpath, index_col=0)
pheno.columns = map(str,pheno.T['taxonomy_name_strains_species'])
pheno=pheno.T
pheno.index.name="new_index"

# drop duplicates
droplist=pheno.index.get_level_values('new_index').get_duplicates()
for dchecked in droplist:
    pheno=pheno.T
    pheno = pheno.drop(dchecked, 1)
    pheno=pheno.T

phylo = pd.read_table('%sCorr_matrix.txt'%inpath, index_col=0)

inlis=list(phylo.index.values)
newin=[]
for n in list(phylo.index.values):
    try:
        newin.append(n.split(".g__")[1].split(".s__")[0]+" "+n.split(".s__")[1].split(".t__")[0])
    except:
        newin.append(n)
phylo['new_index']=newin
phylo = phylo.set_index('new_index')
phylo.columns=newin

# drop duplicates
droplist=phylo.index.get_level_values('new_index').get_duplicates()
for dchecked in droplist:
    phylo = phylo.drop(dchecked, 1)
    phylo=phylo.T
    phylo = phylo.drop(dchecked, 1)
    phylo=phylo.T

#reindex to match
phylo_match, pheno_match = match(phylo, pheno)
phylo_match, pheno_match = match(phylo_match.T, pheno)

pheno.to_csv('%smatched_pheno.csv'%otupath,sep="\t")
phylo.to_csv('%smatched_phylo.csv'%otupath,sep="\t")
