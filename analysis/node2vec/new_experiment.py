import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('exp_name')
parser.add_argument('edgelist_path')
parser.add_argument('weight_var')
args = parser.parse_args()

os.system(f'cp -r template_experiment {args.exp_name}')

for file in ['1_embed_nodes.sh', '3_assess.sh']:
    path = f'{args.exp_name}/{file}'
    with open(path, 'r') as f:
        contents = f.read()
    new_contents = contents.replace('REPLACE_ME_WITH_PATH_TO_TARGET_EDGELIST', args.edgelist_path)
    new_contents = new_contents.replace('REPLACE_ME_WITH_TARGET_WEIGHT_COLUMN_IN_EDGELIST', args.weight_var)
    with open(path, 'w') as f:
        f.write(new_contents)