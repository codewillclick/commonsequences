
import re
import sys
import time

class mark:
	'''
	Keep track of timing.
	'''
	def __init__(self):
		self.marks = []
	def mark(self,s=None):
		t = time.time()
		self.marks.append([s,t])
		return self
	def reset(self):
		self.marks = []
		return self
	def iter(self):
		for i in range(1,len(self.marks)):
			r = self.marks
			if not self.marks[i][0] is None:
				yield [self.marks[i][0], self.marks[i][1]-self.marks[i-1][1]]

class comseq:
	'''
	Class managing the configuration and evaluation of the ordered n-word sequence
	exercise.  Call eval(...) to evaluate against options provided by sys.argv.
	'''
	def __init__(self, norm=None, enkey=None):
		self.reset()
		# These two are only configurable manually, but represent valid word
		# extraction from word blocks within iteration step.
		self.word_regex = r'(\w+(\'\w+)*)'
		self.word_regex_map = lambda r:r[0]
		# norm() is run to normalize key text, forcing it to lowercase in this case.
		if norm:
			self.norm = norm
		else:
			def defnorm(r):
				# Normalize case or any other thing of input list.
				return tuple(map(lambda s:s.lower(),r))
			self.norm = defnorm
		# enkey() specifies how to convert the sequence list or tuple into a key.
		# Tuples are already valid keys, but this simplifies things for rendering
		# purposes.
		if enkey:
			self.enkey = enkey
		else:
			def defenkey(r):
				return ' '.join(r)
			self.enkey = defenkey
	
	def reset(self):
		# Reset class instance variables.
		self.table = {}
		self.word_count = 0
		self.seq_count = 0
	
	def eval(self,count=3,argv=sys.argv):
		# Iterate through all sequences provided input file sources.
		self.reset()
		for r in self.__iter_all(argv=argv,count=3):
			# r is a sequence of size count.
			t = self.norm(r)
			k = self.enkey(t)
			if not k in self.table:
				self.table[k] = 0
				self.seq_count += 1
			self.table[k] += 1
			self.word_count += 1
	
	def __iter_all(self,count=3,argv=sys.argv):
		# Use both input_line_iterator() and iter_word_block() to yield sequences.
		prev = None
		for block in self.__input_line_iterator(argv=argv):
			# Pass prev in to maintain (count-1) words between blocks.
			for r in self.__iter_word_block(block,count=count,prev=prev):
				yield r
				prev = r
	
	def __input_line_iterator(self,argv=sys.argv):
		# Run through files in this list.
		# NOTE: sys.argv logic should be separate from this class.  Consider
		#   passing in a list of files, and have another object or class manage
		#   deciding what sources to use for initial block iteration.
		fr = []
		try:
			if len(argv) > 1:
				# Arguments were provided, so lets read these files in.
				err = []
				for f in argv[1:]:
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

	def __iter_word_block(self,s,count=3,prev=None):
		# Iterate through individual valid words in a word block.
		# - prev: if a previous sequence exists, pass it in through this param
		def lshift(r,s):
			# Shift all elements in an array over one.
			for i in range(count-1):
				r[i] = r[i+1]
			r[-1] = s
			return r
		#tokens = list(map(lambda r:r[0],re.findall(r'(\w+(\'\w+)*)',s)))
		tokens = list(map(self.word_regex_map,re.findall(self.word_regex,s)))
		x = None # starting index for tokens
		# HACK: Use of prev is a hack.  It works, but I'm sure there's a more elegant
		#   way to handle the algorithm than passing a previous entry in.
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
			# r is the same list being reused, so it saves on memory.
			yield r


if __name__ == '__main__':
	
	def display(com,timer=mark(),show=None):
		# Display in a pleasing manner the first X number of most frequented sequences.
		show = show if show else com.seq_count
		def order(t):
			# WARNING: Extremely memory-inefficient.  Consider storing only max values
			#   as it goes.
			return sorted(t.items(),key=lambda a:a[1],reverse=True)
		
		timer.mark()
		ordered = order(com.table)[:show]
		timer.mark('ordered table keys')
		
		# Print some quick summary info to stderr, in case stdout output is piping
		# into some other process.
		if com.word_count >= 0:
			print('word count:',com.word_count, file=sys.stderr)
		print('table entry count:',len(com.table.keys()), file=sys.stderr)
		print('timing:',file=sys.stderr)
		for a,b in timer.iter():
			print('  (%s, %i ms)' % (a,int(b*1000)), file=sys.stderr)
		print(file=sys.stderr)
		
		# Actual output happens here.
		for k,v in ordered:
			print('%i - %s' % (v,k))

	# Set up the evaluating class.
	com = comseq()

	# Run through every sequence.
	m = mark().mark()
	com.eval(count=3, argv=sys.argv)
	m.mark('generated table')
	
	# Show what's what.
	display(com, timer=m, show=100)


