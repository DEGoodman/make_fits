''' NOTE: this file must be executed in the parent directory of the fits files.
'''
import csv
import os

# read list of fits files for input
def get_files():
    path = os.getcwd()
    fits_list = []
    # we will get all files listed in the science metadata tsv
    with open('sci_metadata.tsv','rb') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        # blow away a header
        header = tsvin.readline()
        for row in tsvin:
            fits_list.append(row[0])
            print("Adding %s" % row[0])
    split_files()

# break fits_list into manageable sub lists
def split_files():
    list_breaks=[]
    for i in range(len(fits_list)/10):
        list_breaks[i] = fits_list[i*(len(fits_list)/10):i+1(len(fits_list)/10)]
        print("sublist length: %s" % len(list_breaks[i]))

    print("finished sublisting; len(list_breaks): %s" % len(list_breaks))

# create makeflow file
def write_mf():
    
    # makeflow = open(r'go.mf', 'w')

    #TODO: write makeflow file
    # Get all fits
    # makeflow.write("images : ")
    # loop through SCIENCE
    # for each ^, use fitsavg to get 'closest' DARKs
        # Subtract SCIENCE - DARK(avgs) (<-- fitssub)

if __name__ == "__main__":
    get_files()