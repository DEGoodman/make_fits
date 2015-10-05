''' NOTE: this file must be executed in the parent directory of the fits files.
'''
import csv
import datetime.datetime as datetime
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
    # ewwwwwwwwwwww way to remove header
    for row in tsvin:
        fits_list.append(row[0])
    fits_list.pop(0)

    # setup DARK tsv
    exfile  = open('dark_metadata.tsv','rb')
    tsvdark = csv.reader(exfile, delimiter='\t')

    write_mf(fits_list)
    # close csv
    infile.close()
    exfile.close()

# create makeflow file
def write_mf(fits_list):
    makeflow = open(r'go.makeflow', 'w')
    # loop through SCIENCE fits
    for f in fits_list:
        # get current SCIENCE datetime
        time = get_datetime(f)
        # read in DARK tsv file, find nearest absolute datetimes, return n*fits filemnames 
        dark_fits = getDarks(time)

        # TODO:
        # use fitsavg to get 'closest' DARKs
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

    makeflow.close()

def get_datetime(sci_img):
    if tsvin:
        for row in tsvin:
            if row[0] = sci_img:
                # return datetime
                return timeConv(row[3])
    return datetime.now()

# thanks Ryan Jicha!
def timeConv(time):
    date = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f")
    return date

# get 4 closest dark files
def getDarks(time):
    temp_list = [(None,datetime.now()) for i in range(4)]
    # compare times
    for row in tsvdark:
        if math.fabs(timeConv(row[3])-time) < math.fabs(temp_list[0]-time):
            temp_list[3] = temp_list[2]
            temp_list[2] = temp_list[1]
            temp_list[1] = temp_list[0]
            temp_list[0] = (row(0),timeConv(row[3]))
    # how did we do?
    print("getDarks -> temp_list: %s" % temp_list)
    return temp_list

if __name__ == "__main__":
    get_files()