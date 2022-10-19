#!/bin/bash

mkdir embeds/edges

for file in $(ls embeds/nodes/forwards*)
do
    # Get corresponding file names for this value of p and q
    forwards_walk_file=${file:13}
    pq=${forwards_walk_file:9:-12}
    backwards_walk_file=backwards_$pq\.nodevectors

    # Get edge vectors via all 5 methods 
    outfile_suffix=$pq\.edgevectors
    python ../edge_embed.py embeds/nodes/$forwards_walk_file embeds/nodes/$backwards_walk_file all --out_name $outfile_suffix
    
    # Store output
    mv *$outfile_suffix embeds/edges
done

