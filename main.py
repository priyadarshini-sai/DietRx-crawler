from __future__ import print_function
import os
import numpy as np
import requests
import re,ast
import pandas as pd
import json
from bs4 import BeautifulSoup
from requests.api import get
import time
import argparse
from utils import *


## create food-X(disease,chemical,gene) association list ##

def fetch(type,saver):

    dflist=[]

    ## create food list ##
    if type=="food_list":
        keys = ["id", "category", "scientific_name", "common_names"]
        data_list = var_data_to_dict(food_url)
        for k in range(len(data_list)):
            x = dict(zip(keys,data_list[k][:len(keys)]))
            dflist.append(x)

    ## create disease list ##
    if type=="disease_list":
        keys = ["id", "category", "name", "disease_synonyms"]
        data_list = var_data_to_dict(disease_url)
        for k in range(len(data_list)):
            x = dict(zip(keys,data_list[k][:len(keys)]))
            dflist.append(x)

    ## create chemical list ##
    if type=="chemical_list":
        keys = ["pubChemID", "common_name", "functional_group"]
        data_list = var_data_to_dict(chemical_url)
        for k in range(len(data_list)):
            x = dict(zip(keys,data_list[k][:len(keys)]))
            dflist.append(x)

    ## create gene list ##
    if type=="gene_list":
        keys = ["geneID", "gene_symbol", "gene_name", "gene_other_symbol", "gene_synonyms"]
        data_list = var_data_to_dict(gene_url)
        for k in range(len(data_list)):
            x = dict(zip(keys,data_list[k][:len(keys)]))
            dflist.append(x)

    ## get nC2 combination pairs from food, chemical, disease and gene entities ##
    if type=="food_disease_list":
        data_list = var_data_to_dict(food_url)
        dflist = get_food_disease_relationship(data_list,domain)
    if type=="food_chemical_list":
        data_list = var_data_to_dict(food_url)
        dflist = get_food_chemical_relationship(data_list,domain)
    if type=="food_gene_list":
        data_list = var_data_to_dict(food_url)
        dflist = get_food_gene_relationship(data_list,domain)
    if type=="disease_gene_list":
        data_list = var_data_to_dict(disease_url)
        dflist = get_disease_gene_relationship(data_list,domain)
    if type=="disease_chemical_list":
        data_list = var_data_to_dict(disease_url)
        dflist = get_disease_chemical_relationship(data_list,domain)    
    if type=="chemical_gene_list":
        data_list = var_data_to_dict(chemical_url)
        dflist = get_chemical_gene_relationship(data_list,domain)  

    df = pd.DataFrame(dflist)
    if saver:
        df.to_csv(type+'.csv')
        print('saved file')


def main():
    # argparse thingy
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, default="food_list")
    args = parser.parse_args()
    type = args.type
    saver = 1
    global domain, food_url,chemical_url,disease_url,gene_url
    domain = "https://cosylab.iiitd.edu.in"
    food_url = "https://cosylab.iiitd.edu.in/dietrx/view_all?type=food"
    chemical_url = "https://cosylab.iiitd.edu.in/dietrx/view_all?type=chemical"
    disease_url = "https://cosylab.iiitd.edu.in/dietrx/view_all?type=disease"
    gene_url = "https://cosylab.iiitd.edu.in/dietrx/view_all?type=gene"
       
    fetch(type,saver)

if __name__ == '__main__':
    main()