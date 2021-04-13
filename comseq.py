
import re
import sys

def input_line_iterator():
	# Run through files in this list.
	fr = []
	try:
		if len(sys.argv) > 1:
			# Arguments were provided, so lets read these files in.
			err = []
			for f in sys.argv[1:]:
				try:
					fr.append(open(f,'r'))
				except FileNotFoundError:
					# Add failed reads to a list of errors.
					err.append(f)
			# If any files were unable to be read, cancel the whole thing.
			if len(err):
				raise Exception('Exiting, file(s) not found:\n' + '\n'.join(err))
		else:
			# Read from stdin.
			fr.append(sys.stdin)
		for f in fr:
			# WARNING: A single blob file with no newlines will stuff the RAM full.
			# TODO: Implement a block iterator that crawls along a little every read
			#   block to be sure it has a complete word at its ending character.
			s = f.readline()
			while len(s):
				yield s
				s = f.readline()
			f.close()
	finally:
		for f in fr:
			if not f.closed:
				f.close()

if __name__ == '__main__':
	
	i = 0
	for s in input_line_iterator():
		print('i:%i, [%s]' % (i,s))
		i += 1

