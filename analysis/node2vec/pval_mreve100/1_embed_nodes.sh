#!/bin/bash

mkdir embeds
mkdir embeds/nodes

for p in 0.25 0.5 1 2 4
do
    for q in 0.25 0.5 1 2 4
    do
        for direction in forwards backwards
        do
            python ../node_embed.py \
            ../../../data/processed/subgraphs/mreve_100_nodes.csv \
            --weight_var neglog_pval \
            --out_dir embeds/nodes \
            --p $p \
            --q $q \
            --dimensions 64 \
            --walk_length 25 \
            --walks_per_node 10 \
            --direction $direction
        done
    done
done