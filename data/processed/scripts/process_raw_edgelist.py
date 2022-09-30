import pandas as pd
from numpy import abs, log10
from os import system

raw_dir = '../../raw'

# Read in column names
with open(f'{raw_dir}/mr-eve-mr.header') as f:
    string = f.read()[:-1]
    cols = string.split(',')

# Read edges
edge_df = pd.read_csv(f'{raw_dir}/mr-eve-mr.csv', header=None)
edge_df.columns = cols

# Drop edges with no p-value/effect size
edge_df = edge_df.loc[pd.notna(edge_df.pval)]
edge_df = edge_df.loc[pd.notna(edge_df.b)]

# Deal with 0 p-vals
how = 'next lowest'
if how == 'remove':
    edge_df = edge_df.loc[edge_df.pval != 0]
elif how == 'next lowest':
    min_p = min(edge_df.loc[edge_df.pval != 0].pval)
    zero_idx = edge_df.loc[edge_df.pval == 0].index
    edge_df.pval[zero_idx] = min_p

# Winsorize extreme p-values
winsorize = False
if winsorize:
    cutoff_pval = 5e-10
    edge_df.pval.loc[edge_df.pval < cutoff_pval] = cutoff_pval

# Create weight columns and drop redundant columns
edge_df['neglog_pval'] = -log10(edge_df.pval)
edge_df['abs_effect'] = abs(edge_df.b)
edge_df = edge_df[['head_node', 'tail_node', 'neglog_pval', 'abs_effect']]

# Save
edge_df.to_csv('../mr-eve-edgelist.csv', index=False)