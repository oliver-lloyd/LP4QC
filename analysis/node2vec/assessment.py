import pandas as pd
import multiprocessing as mp
import argparse
from sklearn.linear_model import LinearRegression
from os import listdir


def assess_model_fit(embedding_file, embedding_path, edges_df, out_file):

    # Get meta info
    method = embedding_file.split('_')[0]
    p = float(embedding_file.split('_')[1][1:])
    q = float(embedding_file.split('_')[2][1:-12])

    # Check if results exists, run if not
    results = pd.read_csv(out_file)
    existing = [[row.method, row.p, row.q] for i, row in results.iterrows()]

    if [method, p, q] not in existing:
        # Load and prepare edge vectors
        embeds = pd.read_csv(f'{embedding_path}/{embedding_file}', header=None, index_col=[0, 1])
        embeds = embeds.loc[edges_df.index]  # Index of both is multi-index of dyads
        embeds.dropna(how='all', axis=1, inplace=True)

        # Perform and assess regression
        model = LinearRegression()
        model.fit(embeds, edges_df.weight)
        r2 = model.score(embeds, edges_df.weight)

        # Write result and meta info
        csv_string = ','.join([str(val) for val in [method, p, q, r2]])
        with open(out_file, 'a') as f:
            f.write(csv_string + '\n')
    else:
        print('Skip')


if __name__ == '__main__':

    # Get user args
    parser = argparse.ArgumentParser()
    parser.add_argument('edgelist')
    parser.add_argument('edge_vec_dir')
    parser.add_argument('--weight_var')
    args = parser.parse_args()

    # Read in graph data
    edgelist = pd.read_csv(args.edgelist, index_col=['head_node', 'tail_node'])
    if args.weight_var:
        edgelist['weight'] = edgelist[args.weight_var]
    elif 'weight' not in edgelist.columns:
        raise ValueError('Either "weight" column must exist in edgelist, or pass name of weight column with --weight_var')
    edgelist = edgelist[['weight']]

    # Create results file if doesn't exists
    result_file = 'model_fit_results.csv'
    if result_file not in listdir():
        pd.DataFrame(columns=['method', 'p', 'q', 'R2']).to_csv(result_file, index=False)

    # Set up parallel args
    para_args = [
        [embed_file, args.edge_vec_dir, edgelist, result_file]
        for embed_file in listdir(args.edge_vec_dir)
    ]

    # Assess regression fit of edge weight on edge vector 
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.starmap(assess_model_fit, para_args)
