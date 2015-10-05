import os

# create workflow file
makeflowflow = open(r'go.makeflow', 'w')

#TODO: write makeflow file
# Get all fits
# loop through SCIENCE
# for each ^, use fitsavg to get 'closest' DARKs
    # Subtract SCIENCE - DARK(avgs) (<-- fitssub)
