# Make_fits
ACIC makeflow file/ fitssub project

This project is designed for the Fall 2015 Cyberinfrastructure course at the University of Arizona. 

The program takes a large number of pre-processed astronomical FITS files, finds the nearest dark images for calibration, and generates a makeflow file to calibrate each valid science image using a High-Performance Computing cluster.
It is designed for large volume and heavy computation processes.

### Workflow

1. Download and install Makeflow on HPC in bPic directory.
    (http://ccl.cse.nd.edu/software/tutorials/acic15/makeflow-tutorial.php)

2. Ensure fitssub is installed and functioning correctly in your working directory.
    (https://pods.iplantcollaborative.org/wiki/display/ACIC2015/Compiling+fitssub)

3. Generate a makeflow file!
    Get all fits files
    loop through SCIENCE fits files
    for each ^, use [fitsavg] to get 'closest' DARKs
        Subtract SCIENCE - DARK(avgs) [fitssub]
