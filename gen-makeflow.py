#!/usr/local/bin/python
''' NOTE: this file must be executed in the parent directory of the fits files.
'''
import csv
from datetime import *
import math
import os

dark_list = []

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
    tsvdark = csv.reader(exfile, delimiter='\t')
    next(tsvdark, None) # skip header
    global dark_list
    for row in tsvdark:
        dark_list.append((row[0], timeConv(row[1])))

    write_mf(fits_list)
    # close csvs
    infile.close()
    exfile.close()

# create makeflow file
def write_mf(fits_list):
    makeflow = open(r'go.makeflow', 'w')
    # loop through SCIENCE fits
    for fit in fits_list:
        # read in DARK tsv file, find nearest absolute datetime, return n*fits filenames (currently: 1)
        dark_fits = getDarks(fit[1])

        ''' TODO: for future version
        # create series of dark files passed in to fitsavg
        df = ""
        for i in dark_fits:
                df += str(i[0])
                df + " "

        # use fitsavg to get 'closest' DARKs
        avg_dark = os.system("./fitsavg -i " + df)
        '''
        avg_dark = dark_fits[0]

        ''' append all modified files with '_m_'.
            write out lines to makeflow file in correct format
            makeflow format:

                outfile : infile_1 infile_2
                    command
                \n
        '''
        makeflow.write("_m_" + str(fit[0]) + " : " + str(fit[0]) + " " + str(avg_dark) + " \n")
        makeflow.write("\t./fitsub -i " + str(fit[0]) + " -r " + str(avg_dark) + " > " + "_m_" + str(fit[0]) "\n")
        makeflow.write("\n")

    makeflow.close()

# thanks Ryan Jicha!
def timeConv(time):
    date = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")
    return date

# get 4 closest dark files
def getDarks(time):
    ''' TODO: for future release (n = 4)
    temp_list = [(None,datetime.now()) for i in range(4)]
    # compare times
    for row in dark_list:
        if abs(row[1]-time) < abs(temp_list[0][1]-time):
            temp_list[3] = temp_list[2]
            temp_list[2] = temp_list[1]
            temp_list[1] = temp_list[0]
            temp_list[0] = (row[0],row[1])

    return temp_list
    '''

    # until fitsavg works
    temp_fname = (None, datetime.now())
    for row in dark_list:
        if abs(row[1]-time) < abs(temp_fname[1]-time):
            temp_fname = (row[0],row[1])
    return temp_fname

if __name__ == "__main__":
    get_files()
