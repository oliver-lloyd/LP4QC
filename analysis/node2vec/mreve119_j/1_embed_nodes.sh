#!/bin/bash

mkdir embeds
mkdir embeds/nodes

for p in 0.25 0.5 1 2 4
do
    for q in 0.25 0.5 1 2 4
    do
        for direction in forwards backwards
        do
            outfile=$direction\_p$p\_q$q\.nodevectors
            if ! ls embeds/nodes | grep $outfile
            then
                python ../node_embed.py \
                ../../../data/processed/subgraphs/mreve_119_nodes_j.csv \
                --weight_var abs_effect \
                --out_dir embeds/nodes \
                --p $p \
                --q $q \
                --dimensions 64 \
                --walk_length 25 \
                --walks_per_node 10 \
                --direction $direction
            else
                echo Found node embeddings: $outfile\. Skipping.
            fi
        done
    done
done