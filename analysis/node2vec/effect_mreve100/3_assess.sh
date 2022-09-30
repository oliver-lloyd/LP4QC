#!/bin/bash

python ../assessment.py \
    ../../../data/processed/subgraphs/mreve_100_nodes.csv \
    embeds/edges \
    --weight_var abs_effect