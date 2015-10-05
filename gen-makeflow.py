''' NOTE: this file must be executed in the parent directory of the fits files.
'''
import csv
import datetime.datetime as datetime
import os

# read list of fits files for input
def get_files():
    path = os.getcwd()
    fits_list = []
    # we will get all files listed in the SCIENCE metadata tsv
    for open('sci_metadata.tsv','rb') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            fits_list.append(row[0])
    # ewwwwwwwwwwww way to remove header
    fits_list.pop(0)
    write_mf(fits_list)

# create makeflow file
def write_mf(fits_list):
    makeflow = open(r'go.makeflow', 'w')
    # loop through SCIENCE fits
    for f in fits_list:
        # use fitsavg to get 'closest' DARKs
        # we are arbitrarily choosing n=4

    # get current SCIENCE datetime

    # read in DARK tsv file, find nearest absolute datetimes, return n*fits filemnames 

        
        # avg_dark = fitsavg(f)
        avg_dark = None

        ''' append all modified files with '_m_'.
            write out lines to makeflow file in correct format
            makeflow format:

                outfile : infile_1 infile_2
                    command
                \n
        '''
        makeflow.write("_m_" + f + " : " + f + " " + avg_dark)
        makeflow.write("\t./fitsub -i " + f + avg_dark)
        makeflow.write("\n")
        # Subtract SCIENCE - DARK(avgs) (<-- fitssub)

def get_datetime(sci_img):
    pass

# thanks Ryan Jicha!
def timeConv(time):
    date = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")
    return date


if __name__ == "__main__":
    get_files()