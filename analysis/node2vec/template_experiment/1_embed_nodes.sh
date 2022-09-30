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
            REPLACE_ME_WITH_PATH_TO_TARGET_EDGELIST \
            --weight_var REPLACE_ME_WITH_TARGET_WEIGHT_COLUMN_IN_EDGELIST \
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