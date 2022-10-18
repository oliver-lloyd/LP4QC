import pandas as pd
import argparse
import os
from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser()
parser.add_argument('dataset_name', type=str)
parser.add_argument('binary_edgelists', type=str, nargs='+')
parser.add_argument('--train_proportion', type=float, default=0.8)
args = parser.parse_args()

# Load data
out_edges = pd.DataFrame()
for edgelist_path in args.binary_edgelists:
    temp_df = pd.read_csv(edgelist_path)
    out_edges = out_edges.append(temp_df)

# Split data
train, test_valid = train_test_split(out_edges, test_size=1-args.train_proportion, stratify=out_edges.relation)
test, valid = train_test_split(test_valid, test_size=0.5, stratify=test_valid.relation)

# Save
dir_name = f'../libkge_data/{args.dataset_name}'
os.mkdir(dir_name)
train.to_csv(dir_name + '/train.txt', index=False, header=None, sep='\t')
test.to_csv(dir_name + '/test.txt', index=False, header=None, sep='\t')
valid.to_csv(dir_name + '/valid.txt', index=False, header=None, sep='\t')

# Process for LibKGE
os.system(f'../../../../kge/data/preprocess/preprocess_default.py {dir_name}')