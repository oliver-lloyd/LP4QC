import pandas as pd
from numpy.random import choice

node_traits = pd.read_csv('../../data/raw/attributes/node_attributes.csv')

sampled = []
for consortium in node_traits.consortium.unique():
    if pd.notna(consortium):
        sub_df = node_traits.loc[node_traits.consortium == consortium]
        index = choice(sub_df.index)
        gwas = sub_df.loc[index]
        sampled.append(gwas)

out_df = pd.DataFrame(sampled)
out_df.to_csv('gwas_for_LDSc_reg.csv', index=False)