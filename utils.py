from __future__ import print_function
import numpy as np
import pandas as pd
import json
import requests
import re,ast
import time


def find_between( s, first, last ):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

## create list of entities and their attributes ##
def create_data_list(url,keys):    
    dflist=[]
    req = requests.get(url)
    content = req.text
    get_data=find_between(content,"var data = [","];")
    get_data="["+get_data+"]"
    data_list=json.loads(get_data)    
    data_len = len(data_list)
    for k in range(data_len):
        x = dict(zip(keys,data_list[k][:len(keys)]))
        dflist.append(x)
    return dflist

def var_data_to_dict(url):
    response = requests.get(url)
    if response.status_code!=200:
        print("web site does not exist")
        sys.exit(0)

    content = response.text
    get_data = find_between(content,"var data = [","];")
    get_data="["+get_data+"]"
    data_list=json.loads(get_data)
    return data_list

## create list of entities and their attributes ##
def get_food_disease_relationship(data_list,domain):

    dflist=[]
    pos_neg_key = "(\u003cspan style=\"color: green\"\u003ePositive\u003c/span\u003e, \u003cspan style=\"color: red\"\u003eNegative\u003c/span\u003e, Chemical) Associations"
    data_len = len(data_list)
    # loop on food items
    for k in range(data_len):
        d1 = {}
        disease_id,disease_name,disease_cat = [],[],[]
        pos_neg,chem_association = [],[]

        d1["Food ID"] = data_list[k][0]
        print("food_id: ", data_list[k][0])

        # path to a food-disease association page
        path = domain+"/dietrx/get_food?food_id=Plant+ID%3A"+str(data_list[k][0])+"&subcategory=disease"
        
        response = requests.get(path)
        if response.status_code!=200:
            print("food and disease association info not available for food id ",data_list[k][0])
            continue
        content = response.text
        get_data=find_between(content,"var data = [","];")
        get_data="["+get_data+"]"
        # x is list of dictionary
        x=json.loads(get_data)
        # loop on disease list
        for song in x:
            disease_id.append(song["Disease ID"]["data"])
            disease_name.append(song["Disease Name"]["data"])
            disease_cat.append(song["Disease Category"]["data"])
            pos = song[pos_neg_key]["positive"]
            neg = song[pos_neg_key]["negative"]
            pos_neg.append([pos, neg])
            # link to associated chemicals with disease and food is broken
            # chem_association.append()
        
        d1["Disease ID"]=disease_id
        d1["Disease Name"]=disease_name
        d1["Disease Category"]=disease_cat
        d1["Positive Negative Association"]=pos_neg    
        # d1["Chem Association"]=chem_association
        # print("dictionary: ", d1)
        dflist.append(d1)
        time.sleep(1)
        print(k)
    return dflist

def get_food_chemical_relationship(data_list,domain):
    
    dflist=[]
    data_len = len(data_list)
    # loop on food items
    for k in range(data_len):
        d1 = {}
        pubchem_id,common_name,functional_group = [],[],[]
        Content,source = [],[]

        d1["Food ID"] = data_list[k][0]
        print("food_id: ", data_list[k][0])

        # path to a food-constitutents chemicals association page
        path = domain+"/dietrx/get_food?food_id=Plant+ID%3A"+str(data_list[k][0])+"&subcategory=chemical"
        
        response = requests.get(path)
        if response.status_code!=200:
            print("food and chemical association info not available for food id ",data_list[k][0])
            continue
        content = response.text
        get_data=find_between(content,"var data = [","];")
        get_data="["+get_data+"]"
        # x is list of dictionary
        x=json.loads(get_data)
        # loop on constituent chemical list
        for song in x:
            pubchem_id.append(song["PubChem ID"]["data"])
            common_name.append(song["Common Name"]["data"])
            Content.append(song["Content"]["data"])
            functional_group.append(song["Functional Group"]["data"])
            source.append(song["Source"]["data"])

        
        d1["PubChem ID"]=pubchem_id
        d1["Common Name"]=common_name
        d1["Functional Group"]=functional_group 
        d1["Content"]=Content         
        d1["Source"]=source   

        dflist.append(d1)
        time.sleep(1)
        print(k)
    return dflist

def get_food_gene_relationship(data_list,domain):
    
    dflist=[]
    data_len = len(data_list)
    # loop on food items
    for k in range(data_len):
        d1 = {}
        entrez_gene_id,gene_name,gene_symbol = [],[],[]

        d1["Food ID"] = data_list[k][0]
        print("food_id: ", data_list[k][0])

        # path to a food-gene association page
        path = domain+"/dietrx/get_food?food_id=Plant+ID%3A"+str(data_list[k][0])+"&subcategory=gene"
        
        response = requests.get(path)
        if response.status_code!=200:
            print("food and gene association info not available for food id ",data_list[k][0])
            continue
        content = response.text
        get_data=find_between(content,"var data = [","];")
        get_data="["+get_data+"]"
        # x is list of dictionary
        x=json.loads(get_data)
        # loop on constituent chemical list
        for song in x:
            entrez_gene_id.append(song["Entrez Gene ID"]["data"])
            gene_name.append(song["Gene Name"]["data"])
            gene_symbol.append(song["Gene Symbol"]["data"])
        
        d1["Entrez Gene ID"]=entrez_gene_id
        d1["Gene Name"]=gene_name
        d1["Gene Symbol"]=gene_symbol 
        
        dflist.append(d1)
        time.sleep(1)
        print(k)
    return dflist

def get_disease_gene_relationship(data_list,domain):
    
    dflist=[]
    data_len = len(data_list)
    # loop on disease
    for k in range(data_len):
        d1 = {}
        entrez_gene_id,gene_name,gene_symbol,source,via_chemical = [],[],[],[],[]

        d1["Disease ID"] = data_list[k][0]
        print("Disease ID: ", data_list[k][0])
        id_split = data_list[k][0].split(":")

        # path to a food-gene association page
        path = domain+"/dietrx/get_disease?disease_id="+id_split[0]+"%3A"+str(id_split[1])+"&subcategory=gene"
        
        response = requests.get(path)
        if response.status_code!=200:
            print("disease and gene association info not available for disease id ",data_list[k][0])
            continue
        content = response.text
        get_data=find_between(content,"var data = [","];")
        get_data="["+get_data+"]"
        # x is list of dictionary
        x=json.loads(get_data)
        # loop on constituent chemical list
        for song in x:
            entrez_gene_id.append(song["Entrez Gene ID"]["data"])
            gene_name.append(song["Gene Name"]["data"])
            gene_symbol.append(song["Gene Symbol"]["data"])
            source.append(song["Source"]["data"])
            via_chemical.append(song["Via Chemicals"]["data"])
        
        d1["Entrez Gene ID"]=entrez_gene_id
        d1["Gene Name"]=gene_name
        d1["Gene Symbol"]=gene_symbol 
        d1["Source"]=source
        d1["Via Chemicals"]=via_chemical 
        
        dflist.append(d1)
        time.sleep(1)
        print(k)
    return dflist


def get_disease_chemical_relationship(data_list,domain):
    
    dflist=[]
    data_len = len(data_list)
    # loop on disease
    for k in range(data_len):
        d1 = {}
        pubchem_id,common_name,functional_group = [],[],[]
        via_genes,source,type = [],[],[]

        d1["Disease ID"] = data_list[k][0]
        print("Disease ID: ", data_list[k][0])
        id_split = data_list[k][0].split(":")

        # path to a food-gene association page
        path = domain+"/dietrx/get_disease?disease_id="+id_split[0]+"%3A"+str(id_split[1])+"&subcategory=chemical"
        
        response = requests.get(path)
        if response.status_code!=200:
            print("disease and chemical association info not available for disease id ",data_list[k][0])
            continue
        content = response.text
        get_data=find_between(content,"var data = [","];")
        get_data="["+get_data+"]"
        # x is list of dictionary
        x=json.loads(get_data)
        # loop on constituent chemical list
        for song in x:
            pubchem_id.append(song["PubChem ID"]["data"])
            common_name.append(song["Common Name"]["data"])
            functional_group.append(song["Functional Group"]["data"])
            source.append(song["Source"]["data"])
            via_genes.append(song["Via Genes"]["data"])
            type.append(song["Type"]["data"])
        
        d1["PubChem ID"]=pubchem_id
        d1["Common Name"]=common_name
        d1["Functional Group"]=functional_group 
        d1["Source"]=source
        d1["Via Genes"]=via_genes
        d1["Type"]=type 
        
        dflist.append(d1)
        time.sleep(1)
        print(k)
    return dflist


def get_chemical_gene_relationship(data_list,domain):
    
    dflist=[]
    data_len = len(data_list)
    # loop on disease
    for k in range(data_len):
        d1 = {}
        entrez_gene_id,gene_name,gene_symbol,via_diseases = [],[],[],[]

        d1["PubChem ID"] = data_list[k][0]
        print("PubChem ID: ", data_list[k][0])

        # path to a food-gene association page
        path = domain+"/dietrx/get_chemical?pubchem_id="+str(data_list[k][0])+"&subcategory=gene"
        
        response = requests.get(path)
        if response.status_code!=200:
            print("chemical and gene association info not available for pubchem id ",data_list[k][0])
            continue
        content = response.text
        get_data=find_between(content,"var data = [","];")
        get_data="["+get_data+"]"
        # x is list of dictionary
        x=json.loads(get_data)
        # loop on constituent chemical list
        for song in x:
            entrez_gene_id.append(song["Entrez Gene ID"]["data"])
            gene_name.append(song["Gene Name"]["data"])
            gene_symbol.append(song["Gene Symbol"]["data"])
            via_diseases.append(song["Via Diseases"]["data"])
        
        d1["Entrez Gene ID"]=entrez_gene_id
        d1["Gene Name"]=gene_name
        d1["Gene Symbol"]=gene_symbol 
        d1["Via Diseases"]=via_diseases 
        
        dflist.append(d1)
        time.sleep(1)
        print(k)
    return dflist
