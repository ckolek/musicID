#!usr/bin/env python
__author__ = 'jfeinberg_Deniz'

import sys, getopt, os

from sys import argv
from wave.waveData import WaveData
from wave.waveDataReader import WaveDataReader
from WaveDataComparator import WaveDataComparator
from util.exceptions import InvalidFormatError

"""
Main class that runs all of the components of the dan audio matching program.
"""
class dan:
    def run(self):
        checkInput(self)
        try:
            wave1 = read_wave_data(file1)
        except InvalidFormatError:
            print "ERROR: Invalid file format, file may be mislabelled."
            sys.exit(2)

        try:
            wave2 = read_wave_data(file2)
        except InvalidFormatError:
            print "ERROR: Invalid file format, file may be mislabelled."
            sys.exit(2)

        comp = WaveDataComparator(wave1, wave2)
        if comp.areMatching():
            print "MATCH " + file1 + " " + file2
        else:
            print "NO MATCH"

        return 0

def checkInput(self):
    # Declare variables to hold the files that are passed in to global scope
    global file1
    global file2
    file1 = None
    file2 = None

    # Parse command line input
    try:
        # Get everything on the command line after the file name
        # getopt returns the options and arguments as two separate arrays
        opts, args = getopt.getopt(argv[1:], 'hf:', ['help'])

        # If the user does not use the proper syntax, tell them they
        # have entered the wrong input and exit
        if len(opts) < 2:
            print ("ERROR: Incorrect input. Input two file paths with the -f option "
                   "front of each file\n")
            sys.exit(2)

        # If no options are provided notify the user
        if not opts:
            print ('ERROR: No tags provided. Please precede each file name with the '
                   '-f tag\n')
    # If there is an error, print it out and exit
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    # Loop through the resulting options and arguments
    for o, a in opts:
        # If the user asks for help, print out the usage function to tell them
        # what to do
        if o in ('-h', '--help'):
            usage()
        # Otherwise they are passing in a file location
        elif o in ('-f'):
            # If the file location is valid
            if os.path.exists(a):
                # If it is the first file, assign the argument to the file1
                # variable
                if file1 is None:
                    file1 = a
                # Otherwise, assign the argument to the file2 variable
                else:
                    file2 = a
            # Otherwise, tell the user that the file at the location does not
            # exist
            else:
                print "ERROR: File location does not exist\n"
                sys.exit(2)
        else:
            sys.exit(2)

        # Check if the files is .wav
        if not a[len(a)-4:len(a)] == ".wav":
            print "ERROR: " + a + " is not a supported format\n"
            sys.exit(2)

def usage():
    print "\nThis is the CLI for the dan audio matcher program\n"
    print 'Usage: ' + argv[0] + ' -f <file1> -f <file2>'

def read_wave_data(file_name):
    with WaveDataReader.open(file_name) as reader:
        return reader.read()

# Call main function			
if __name__ == "__main__":
    _dan = dan()

    status = _dan.run()

    sys.exit(status)