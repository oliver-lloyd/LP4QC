import requests
import pandas as pd
import yaml
from time import sleep
from os import listdir
from itertools import combinations
from random import shuffle

with open('../../data/raw/trait_IDs.txt') as f:
    traits = f.read().split('\n')[:-1]

cypher_endpoint = 'https://api.epigraphdb.org/cypher'


# Get genetic correlation data
out_file = 'gen_cor.csv'
try:
    gen_cor = pd.read_csv(out_file)
except FileNotFoundError:
    gen_cor = pd.DataFrame(columns=['trait1', 'trait2', 'rg', 'rg_SE'])
    gen_cor.to_csv(out_file, index=False)
for i, trait in enumerate(traits):
    if trait not in gen_cor.trait1.values:
        query = "MATCH (trait:Gwas)-[gc:GEN_COR]-(assoc_trait:Gwas) " 
        query += f"WHERE trait.id = \"{trait}\" "
        query += "RETURN assoc_trait { .id }, gc { .rg, .rg_SE } "
        response = requests.post(cypher_endpoint, json={'query':query}).json()
        if not response['metadata']['empty_results']:
            print(i, trait)
            to_store = [[trait, res['assoc_trait']['id'], res['gc']['rg'], res['gc']['rg_SE']] for res in response['results']]
        else:
            print(i, 'No results')
            to_store = [[trait, None, None, None]]
        pd.DataFrame(to_store).to_csv(out_file, index=False, mode='a', header=None)


# Get observation correlation data 
out_file = 'obs_cor.csv'
try:
    obs_cor = pd.read_csv(out_file)
except FileNotFoundError:
    obs_cor = pd.DataFrame(columns=['trait1', 'trait2', 'cor'])
    obs_cor.to_csv(out_file, index=False)
for i, trait in enumerate(traits):
    if trait not in obs_cor.trait1.values:
        query = "MATCH (trait:Gwas)-[obs_cor:OBS_COR]-(assoc_trait:Gwas) "
        query += f"WHERE trait.id = \"{trait}\" "
        query += "RETURN assoc_trait {.id, .trait}, obs_cor {.cor}"
        response = requests.post(cypher_endpoint, json={'query':query}).json()
        if not response['metadata']['empty_results']:
            print(i, trait)
            to_store = [[trait, res['assoc_trait']['id'], res['obs_cor']['cor']] for res in response['results']]
        else:
            print(i, 'No results')
            to_store = [[trait, None, None]]
        pd.DataFrame(to_store).to_csv(out_file, index=False, mode='a', header=None)


# Get pairwise literature data (quadratic complexity so only do for nodes for whom we have oc and gc data)
gen_cor = pd.read_csv('gen_cor.csv')
gen_cor.dropna(how='any', axis=0, inplace=True)
gc_nodes = set.union(set(gen_cor.trait1.unique()), set(gen_cor.trait2.unique()))
del gen_cor

obs_cor = pd.read_csv('obs_cor.csv')
obs_cor.dropna(how='any', axis=0, inplace=True)
obs_nodes = set.union(set(obs_cor.trait1.unique()), set(obs_cor.trait2.unique()))
del obs_cor

nodes = set.intersection(gc_nodes, obs_nodes)
trait_pairs = list(combinations(nodes, 2))
lit_data = {}
for i, dyad in enumerate(trait_pairs):
    trait1 = dyad[0]
    trait2 = dyad[1]
    url = 'https://api.epigraphdb.org/literature/gwas/pairwise?gwas_id={trait1}&assoc_gwas_id={trait2}&by_gwas_id=true&pval_threshold=0.1&semmantic_types=&blacklist=false&fuzzy=false'
    response = requests.get(url).json()
    if not response['metadata']['empty_results']:
        print(i, trait)
        lit_data[trait] = response['results']
    else:
        print(i, 'No results')

if len(lit_data) > 0:
    with open('lit_data.yml', 'w') as outfile:
        yaml.dump(lit_data, outfile, default_flow_style=False)