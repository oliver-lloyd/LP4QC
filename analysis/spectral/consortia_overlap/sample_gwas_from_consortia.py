import pandas as pd
from numpy.random import choice

node_traits = pd.read_csv('../../../data/raw/node_attributes/node_attributes.csv')

sampled = []
for consortium, cons_df in node_traits.groupby('consortium'):
    for population, cons_pop_df in cons_df.groupby('population'):
        index = choice(cons_pop_df.index)
        gwas = cons_pop_df.loc[index]
        sampled.append(gwas)

out_df = pd.DataFrame(sampled)
out_df.to_csv('gwas_for_LDSc_reg.csv', index=False)