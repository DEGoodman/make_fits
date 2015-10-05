''' NOTE: this file must be executed in the parent directory of the fits files.
'''
import csv
from datetime import *
import math
import os

tsvin = None
tsvdark = None

# read list of fits files for input
def get_files():
    path = os.getcwd()
    fits_list = []
    # we will get all files listed in the SCIENCE metadata tsv
    infile  = open('sci_metadata.tsv','rb')
    tsvin = csv.reader(infile, delimiter='\t')

    next(tsvin, None) # skip header
    for row in tsvin:
        fits_list.append((row[0], timeConv(row[1])))

    # setup DARK tsv
    exfile  = open('dark_metadata.tsv','rb')
    global tsvdark 
    tsvdark = csv.reader(exfile, delimiter='\t')

    write_mf(fits_list)
    # close csv
    infile.close()
    exfile.close()

# create makeflow file
def write_mf(fits_list):
    makeflow = open(r'go.makeflow', 'w')
    # loop through SCIENCE fits
    for fit in fits_list:
        # get current SCIENCE datetime
        # time = get_datetime(fit)
        # read in DARK tsv file, find nearest absolute datetimes, return n*fits filemnames 
        dark_fits = getDarks(fit[1])

        # use fitsavg to get 'closest' DARKs
        avg_dark = os.system("./fitsavg -i " + dark_fits)

        ''' append all modified files with '_m_'.
            write out lines to makeflow file in correct format
            makeflow format:

                outfile : infile_1 infile_2
                    command
                \n
        '''
        makeflow.write("_m_" + fit[0] + " : " + fit[0] + " " + avg_dark)
        makeflow.write("\t./fitsub -i " + fit[0] + " " + avg_dark)
        makeflow.write("\n")
        # Subtract SCIENCE - DARK(avgs) (<-- fitssub)

    makeflow.close()

# thanks Ryan Jicha!
def timeConv(time):
    date = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")
    return date

# get 4 closest dark files
def getDarks(time):
    temp_list = [(None,datetime.now()) for i in range(4)]
    # compare times
    for row in tsvdark:
        if math.fabs(timeConv(row[1])-time) < math.fabs(temp_list[0]-time):
            temp_list[3] = temp_list[2]
            temp_list[2] = temp_list[1]
            temp_list[1] = temp_list[0]
            temp_list[0] = (row[0],timeConv(row[1]))
    # how did we do?
    print("getDarks -> temp_list: %s" % temp_list)
    return temp_list

if __name__ == "__main__":
    get_files()