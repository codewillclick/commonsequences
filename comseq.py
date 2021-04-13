
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
		# Close any unclosed file out.
		for f in fr:
			if not f.closed:
				f.close()

# WARNING: Woops.  New blocks don't keep the previous tokens, so line breaks
#   end up destroying things.  Need to rethink this.

def iter_word_block(s,count=3,prev=None):
	# NOTE: Look up re.findall performance when you get a chance.  This should
	#   work fine so long as the input block isn't enormous.
	def lshift(r,s):
		# Shift all elements in an array over one.
		# NOTE: A mod array would do this efficiently, but again, let's wait before
		#   implementing the fancy.
		for i in range(count-1):
			r[i] = r[i+1]
		r[-1] = s
		return r
	tokens = list(map(lambda r:r[0],re.findall(r'(\w+(\'\w+)*)',s)))
	x = None
	if prev:
		# If previous values are provided...
		r = [None] + prev[-(count-1):]
		x = 0
	else:
		r = [None] + tokens[:count-1] # going to lshift once
		x = count-1
	for i in range(x,len(tokens)):
		s = tokens[i]
		lshift(r,s)
		yield r
	

def iter_all(count=3,table={}):
	prev = None
	for block in input_line_iterator():
		for r in iter_word_block(block,count=count,prev=prev):
			yield r
			prev = r

if __name__ == '__main__':
	
	table = {}

	# Run through every sequence.
	for r in iter_all(count=3,table=table):
		print('r',r)
		

