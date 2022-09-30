import pandas as pd
import numpy as np
import argparse
import multiprocessing as mp

def get_edge_vec(how, head_vec, tail_node_matrix):

    head_node = head_vec.pop(0)
    tail_nodes = tail_node_matrix.copy().pop(0)

    # Do calculation. First four options suggested by Grover et al
    if how == 'average':
        edge_mat = (head_vec + tail_node_matrix) / 2
    elif how == 'hadamard':
        edge_mat = head_vec * tail_node_matrix
    elif how == 'L1': 
        edge_mat = np.abs(head_vec - tail_node_matrix)
    elif how == 'L2':
        edge_mat = (head_vec - tail_node_matrix)**2
    elif how == 'subtract':
        edge_mat = head_vec - tail_node_matrix
    else:
        raise ValueError(f'Unsuported method: {how}')

    # Add node labels and rearrange columns
    old_columns = edge_mat.columns
    edge_mat['head_node'] = head_node
    edge_mat['tail_node'] = tail_nodes
    edge_mat = edge_mat[['head_node', 'tail_node'] + list(old_columns)]

    return edge_mat

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('head_embeds')
    parser.add_argument('tail_embeds')
    parser.add_argument('methods', nargs='+', choices=['all', 'average', 'hadamard', 'L1', 'L2', 'subtract'])
    parser.add_argument('--out_name', default=None)
    args = parser.parse_args()

    # Read node embeddings fron .nodevector files
    head_embeds = pd.read_csv(args.head_embeds, header=None, sep=' ', skiprows=1)
    tail_embeds = pd.read_csv(args.tail_embeds, header=None, sep=' ', skiprows=1)

    # Parse chosen methods
    if 'all' in args.methods:
        methods = ['average', 'hadamard', 'L1', 'L2', 'subtract']
    else:
        methods = args.methods

    # Loop through methods
    for method in methods:
        print(f'Creating edge vectors via method "{method}"')

        # Set up arguments for parallel processing
        para_args = [
            [method, row, tail_embeds] 
            for i, row in head_embeds.iterrows() 
        ]

        # Do calculations
        with mp.Pool(mp.cpu_count()) as pool:
            matrices = pool.starmap(get_edge_vec, para_args)

        # Save
        out_df = pd.concat(matrices)
        if not args.out_name:
            out_df.to_csv(f'{method}_edge_vectors.csv', header=None, index=False)
        else:
            out_df.to_csv(f'{method}_{args.out_name}', header=None, index=False)


