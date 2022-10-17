import pandas as pd
import argparse
import multiprocessing as mp
from glob import glob
from numpy.random import choice

def parallel_edge_query(edgelist_df, sample_nodes):
    edges = edgelist_df.query('head_node in @sample_nodes and tail_node in @sample_nodes')
    return edges

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('n_nodes', type=int)
    parser.add_argument('--out_name', type=str)
    args = parser.parse_args()

    if not args.out_name:
        out_name = f'mreve_{args.n_nodes}_nodes.csv'
    else:
        out_name = args.out_name

    # Check for intended overwrite
    if glob(out_name):
        print(f'File: {out_name} already exists. Type "yes" to resample or anything else to exit:')
        cont = input().lower()
        if cont != 'yes':
            print('Exiting.')
            quit()

    # Sample n nodes
    print('Sampling nodes..')
    with open('../../raw/trait_IDs.txt') as f:
        txt = f.read()[:-1]
        traits = txt.split('\n')
    sample_traits = choice(traits, args.n_nodes, replace=False)

    # Get relevant edges
    print('Selecting sample edges. This will take a few moments..')
    para_args = [
        [partial_edgelist, sample_traits] 
        for partial_edgelist in pd.read_csv('../mr-eve-edgelist.csv', chunksize=100000)
    ]
    with mp.Pool(mp.cpu_count()) as pool:
        query_results = pool.starmap(parallel_edge_query, para_args)

    # Save
    print('Saving..')
    out_df = pd.DataFrame()
    for edges in query_results:
        if len(edges) > 0:
            out_df = out_df.append(edges)
    out_df.to_csv('../subgraphs/' + out_name, index=False)
    print('Done.')