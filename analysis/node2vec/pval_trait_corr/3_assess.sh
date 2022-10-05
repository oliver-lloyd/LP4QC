#!/bin/bash

python ../assessment.py \
    ../../baseline_prediction/MR_obscor_gencor_edgelist.csv \
    embeds/edges \
    --weight_var neglog_pval