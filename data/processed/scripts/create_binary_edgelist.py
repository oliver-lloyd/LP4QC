import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('weight_var', type=str)
parser.add_argument('threshold', type=float)
parser.add_argument('--less_than', action='store_true')
parser.add_argument('--edgelist', type=str, default='../mr-eve-edgelist.csv')
args = parser.parse_args()

# Read edges
edgelist = pd.read_csv(args.edgelist)

# Perform thresholding
if args.less_than:
    out_edges = edgelist.loc[edgelist[args.weight_var] < args.threshold]
else:
    out_edges = edgelist.loc[edgelist[args.weight_var] > args.threshold]
edge_name = f"{args.weight_var}_{'lessthan' if args.less_than else 'greaterthan'}_{str(args.threshold)}"

# Save
out_edges['relation'] = edge_name
out_edges = out_edges[['head_node', 'relation', 'tail_node']]
out_edges.to_csv(f'../binary_graphs/{edge_name}.csv', index=False)