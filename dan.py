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

file1 = None
file2 = None	
	
def main():
	global file1
	global file2
	try:
		opts, args = getopt.getopt(argv[1:], 'hf:', ['help'])
		if not opts:
			print 'No tags provided. Please precede each file name with the -f tag'
			usage()
	except getopt.GetoptError as err:
		print str(err)
		usage()
		sys.exit(2);
	
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			usage()
			sys.exit(2)
		elif opt in ('-f'):
			if os.path.exists(arg):
				if file1 is None:
					file1 = arg
					print "File Exists"
					print os.path.basename(arg)
				else:
					file2 = arg
					print "File Exists"
					print os.path.basename(arg)
		else:
			usage()
			sys.exit(2);

			
if __name__ == "__main__":
	main();
			
			