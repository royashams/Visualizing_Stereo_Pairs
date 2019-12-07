#!/bin/sh

# PLEASE INSTALL IMAGEMAGICK BEFORE RUNNING THIS SCRIPT! :) Otherwise cannot convert from pfm to png. 
# echo "First arg: $1"
# echo "Second arg: $2"
# echo "Third arg: $3"
cd ./MiddEval3/alg-ELAS
./run $1 $2 2 results
cp -p ./results/disp0.pfm ./../../results
cd ./../../
magick convert ./results/disp0.pfm ./MiddleburyDisparity/$3_binary_disp.png

