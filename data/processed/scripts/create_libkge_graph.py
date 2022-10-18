import pandas as pd
import argparse
import os
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser()
parser.add_argument('weight_var', type=str)
parser.add_argument('threshold', type=float)
parser.add_argument('--less_than', action='store_true')
args = parser.parse_args()

edgelist = pd.read_csv('../mr-eve-edgelist.csv')
if args.less_than:
    out_edges = edgelist.loc[edgelist[args.weight_var] < args.threshold]
else:
    out_edges = edgelist.loc[edgelist[args.weight_var] > args.threshold]

# Prepare edgelist
edge_name = f"{args.weight_var}_{'lessthan' if args.less_than else 'greaterthan'}_{str(args.threshold)}"
out_edges['relation'] = edge_name
out_edges = out_edges[['head_node', 'relation', 'tail_node']]

# Split data
train, test_valid = train_test_split(out_edges, test_size=0.2)
test, valid = train_test_split(test_valid, test_size=0.5)

# Save
os.mkdir(f'../binary_graphs/{edge_name}')
train.to_csv('../binary_graphs/' + edge_name + '/train.txt', index=False, header=None, sep='\t')
test.to_csv('../binary_graphs/' + edge_name + '/test.txt', index=False, header=None, sep='\t')
valid.to_csv('../binary_graphs/' + edge_name + '/valid.txt', index=False, header=None, sep='\t')

# Process for LibKGE
os.system(f'../../../../kge/data/preprocess/preprocess_default.py ../binary_graphs/{edge_name}')