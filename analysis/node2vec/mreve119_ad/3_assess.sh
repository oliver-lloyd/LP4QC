#!/bin/bash

python ../assessment.py \
    ../../data/processed/subgraphs/mreve_119_nodes_ad.csv \
    embeds/edges \
    --weight_var abs_effect