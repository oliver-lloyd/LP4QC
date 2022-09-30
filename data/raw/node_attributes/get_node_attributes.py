import pandas as pd
import ieugwaspy as gwas
import requests
from time import sleep

def chunker(iter, size=50):
    current = 0
    while current < len(iter):
        yield iter[current: current+size]
        current += size

if __name__ == '__main__':
    with open('../trait_IDs.txt') as f:
        contents = f.read()
        traits = contents.split('\n')[:-1]

    responses = []
    for trait_list in chunker(traits):
        response = requests.get('http://gwas-api.mrcieu.ac.uk/gwasinfo/' + ','.join(trait_list))
        responses += response.json()
        sleep(0.1)


    out = pd.DataFrame(responses)
    out = out[['id'] + [col for col in out.columns if col != 'id']]
    out.consortium.loc[out.consortium == 'BioBank Japan Project'] = 'Biobank Japan Project'
    out.to_csv('node_attributes.csv', index=False)