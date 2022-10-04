#!/bin/bash

# Get data
wget http://opsahl.co.uk/tnet/datasets/USairport_2010.txt

# Convert to CSV for consistency
touch USairport_2010.csv
echo head_node,tail_node,weight >> USairport_2010.csv
sed 's/ /,/g' USairport_2010.txt >> USairport_2010.csv