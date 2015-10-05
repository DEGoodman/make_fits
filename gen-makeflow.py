''' NOTE: this file must be executed in the parent directory of the fits files.
'''
import csv
import os

# read list of fits files for input
def get_files():
    path = os.getcwd()
    fits_list = []
    # we will get all files listed in the SCIENCE metadata tsv
    with open('sci_metadata.tsv','rb') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        # blow away a header
        header = tsvin.readline()
        for row in tsvin:
            fits_list.append(row[0])
            print("Adding %s" % row[0])
    # write_mf(fits_list)

# create makeflow file
def write_mf(fits_list):
    makeflow = open(r'go.makeflow', 'w')
    # loop through SCIENCE fits
    for f in fits_list:
        # use fitsavg to get 'closest' DARKs
        # TODO: get list of FITS files for acg
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

if __name__ == "__main__":
    get_files()