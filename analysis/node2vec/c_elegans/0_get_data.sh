#!/bin/bash

# Get data
wget http://opsahl.co.uk/tnet/datasets/celegans_n306.txt

# Convert to CSV for consistency
touch celegans_n306.csv
echo head_node,tail_node,weight >> celegans_n306.csv
sed 's/ /,/g' celegans_n306.txt >> celegans_n306.csv