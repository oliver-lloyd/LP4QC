import pandas as pd
import networkx as nx
import argparse
from node2vec import Node2Vec
from multiprocessing import cpu_count

# Read arguments
parser = argparse.ArgumentParser()
parser.add_argument('edgelist', type=str)
parser.add_argument('--weight_var', type=str)
parser.add_argument('--p', type=float, default=1)
parser.add_argument('--q', type=float, default=1)
parser.add_argument('--dimensions', type=int, default=64)
parser.add_argument('--walk_length', type=int, default=25)
parser.add_argument('--walks_per_node', type=int, default=10)
parser.add_argument('--direction', type=str, default='forwards')
parser.add_argument('--out_dir', type=str)
args = parser.parse_args()

# Read in edges
edgelist = pd.read_csv(args.edgelist)
if args.weight_var:
    edgelist['weight'] = edgelist[args.weight_var]
elif 'weight' not in edgelist.columns:
    raise ValueError('Either "weight" column must exist in edgelist, or pass name of weight column with --weight_var')
edgelist = edgelist[['head_node', 'tail_node', 'weight']]

# Prepare graph
if args.direction == 'forwards':
    graph_type = nx.DiGraph
elif args.direction == 'backwards':
    graph_type = nx.DiGraph
    edgelist.columns = ['tail_node', 'head_node', 'weight']  # Swap head and tail columns for backwards directed walks
elif args.direction == 'undirected':
    graph_type = nx.Graph
g = nx.from_pandas_edgelist(edgelist, 'head_node', 'tail_node', edge_attr='weight', create_using=graph_type)
del edgelist

# Precompute probabilities and generate walks
node2vec = Node2Vec(
    g, 
    dimensions=args.dimensions, 
    walk_length=args.walk_length, 
    num_walks=args.walks_per_node, 
    workers=cpu_count()
)  

# Embed nodes
model = node2vec.fit(min_count=0)
node_vectors = model.wv
del model

# Save vectors
out_path = f'{args.direction}_p{args.p}_q{args.q}.nodevectors'
if args.out_dir:
    out_path = f'{args.out_dir}/{out_path}'
node_vectors.save_word2vec_format(out_path)

