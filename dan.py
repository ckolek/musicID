__author__ = 'jfeinberg'

import sys, getopt, os


from sys import argv
from wave.waveData import WaveData
from wave.waveDataReader import WaveDataReader
from WaveDataComparator import WaveDataComparator

""" Main class for comparing two wave files
Usage provides basic description of the program\n
Main handles input parsing
"""

def usage():
	print "\nThis is the CLI for the dan audio matcher program\n"
	print 'Usage: ' + argv[0]+ ' -f <file1> -f <file2>'

# Declare variables to hold the files that are passed in	
file1 = None
file2 = None	
	
	
def main():
	# Set variables to global scope
	global file1
	global file2
	# Parse command line input
	try:
		# Get everything on the command line after the file name
		# getopt returns the options and arguments as two separate arrays
		opts, args = getopt.getopt(argv[1:], 'hf:', ['help'])
		 
		# If the user does not use the proper syntax, tell them they 
		# have entered the wrong input and exit
		if len(opts) < 2:	
			print ("Incorrect input. Input two file paths with the -f option "
					"front of each file")
			usage()
			sys.exit(2)
		
		# If no options are provided notify the user
		if not opts:
			print ('No tags provided. Please precede each file name with the '
					'-f tag')
			usage()
	# If there is an error, print it out and exit
	except getopt.GetoptError as err:
		print str(err)
		usage()
		sys.exit(2)
	
	# Loop through the resulting options and arguments
	for o, a in opts:
		print o
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
					# Debug stuff
					print "File Exists"
					print os.path.basename(a)
				# Otherwise, assign the argument to the file2 variable
				else:
					file2 = a
					# More debug
					print "File Exists"
					print os.path.basename(a)
			# Otherwise, tell the user that the file at the location does not 
			# exist
			else:
				print "File location does not exist"
				usage()
				sys.exit(2)
		else:
			usage()
			sys.exit(2)

# Call main function			
if __name__ == "__main__":
	main()
			
			