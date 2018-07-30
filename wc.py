import sys
import argparse

#We override the error() method of ArgumentParser, to get wc look-alikeness, regarding
#the wrong flag error messages
class WcParser(argparse.ArgumentParser):
	def error(self, message):
		wrong_arg = message.split()[-1]
		if wrong_arg.startswith('-') or wrong_arg.startswith("'"):
			err=""
			if wrong_arg.startswith('--'):
				err = "wc: unrecognized option '"+ wrong_arg +"'\nTry 'wc --help' for more information." 
			else:
				err = "wc: invalid option -- '"+ wrong_arg[1] +"'\nTry 'wc --help' for more information."
			raise ValueError(err)

def arg_parse( inp ):
	
	"""
        This function uses Python’s argparse module to parse the input list and generate the
	count options depending on the flags present. It also returns the file operands in a seperate list.

        :param inp: A list which contains flags and file operands
        :return:  A list of boolean values which contains count options and a list which contains the file
		operands, or an error message if a flag was unknown.
        """	
	
	parser = WcParser()
	parser.add_argument("-l", "--lines", action="store_true",help="print the newline counts")
	parser.add_argument("-w", "--words", action="store_true",help="print the word counts")
	parser.add_argument("-c", "--bytes", action="store_true",help="print the byte counts")
	parser.add_argument("-m", "--chars", action="store_true",help="print the character counts")
	parser.add_argument("-L", "--max_line_length", action="store_true",help="print the maximum display width")
	parser.add_argument("--version", action="store_true",help="output version information and exit")
	parser.add_argument("files", help="input files", nargs="*")

	try:	
		args = parser.parse_args(inp)
	except ValueError as e:
		return str(e)

	flags = [args.lines, args.words, args.chars, args.bytes, args.max_line_length]
	
	if args.lines == False and args.words == False and args.bytes == False and args.chars == False and args.max_line_length == False:
		flags = [True,True,False,True,False]
		
	files=args.files[1:]

	if args.version:
		version = "wc (GNU coreutils) 8.25\nCopyright (C) 2016 Free Software Foundation, Inc.\nLicense GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.\nThis is free software: you are free to change and redistribute it.\nThere is NO WARRANTY, to the extent permitted by law.\n\nWritten by Paul Rubin and David MacKenzie.\n"
		return version
	
	return flags, files

def counter( f,is_stdin ):

	"""
        This function executes the counting part of the program. If is_stdin is True, then line
	count is reduced by one (to simulate real wc’s behaviour), else it is returned as it is, accompained by
	all the other counts.

        :param f: A file descriptor or data from stdin input 
	:param is_stdin: a boolean value which specifies if stdin mode is on.
        :return:  A collection of all the possible counts from the file contents or stdin input
        """

	num_lines, num_words, num_bytes, num_chars, max_width = 0,0,0,0,0
	line_widths = []
	for line in f:
		num_lines += 1
		num_words += len(line.split())
		num_bytes += len(line.encode('utf-8'))
		num_chars += len(line)
		line_widths.append(len(line) - 1)
	
	if len(line_widths) > 0:
		max_width = max(line_widths)
	if is_stdin and num_lines > 0:
		return num_lines-1, num_words, num_chars, num_bytes, max_width
	else:
		return num_lines, num_words, num_chars, num_bytes, max_width


def arg_handling( inp ):

	"""
        This function preprocesses the raw input from sys.argv and handles the –files0-from=F
	option of the program, getting all the file operands from the F file. Then, It calls arg_parse() to get
	the count options.

        :param inp: The raw input from sys.argv
        :return:  A list of boolean values which contains count options and a list which contains the file
		operands, or an error message if an error happened(for example flag was unknown).
        """
	
	for j in inp:
		if j == "--help":
			outp = "Usage: wc [OPTION]... [FILE]...\n  or:  wc [OPTION]... --files0-from=F\nPrint newline, word, and byte counts for each FILE, and a total line if\nmore than one FILE is specified.  With no FILE, or when FILE is -,\nread standard input.  A word is a non-zero-length sequence of characters\ndelimited by white space.\nThe options below may be used to select which counts are printed, always in\nthe following order: newline, word, character, byte, maximum line length.\n  -c, --bytes            print the byte counts\n  -m, --chars            print the character counts\n  -l, --lines            print the newline counts\n      --files0-from=F    read input from the files specified by\n                           NUL-terminated names in file F;\n                           If F is - then read names from standard input\n  -L, --max-line-length  print the length of the longest line\n  -w, --words            print the word counts\n      --help     display this help and exit\n      --version  output version information and exit\n\nReport wc bugs to bug-coreutils@gnu.org\nGNU coreutils home page: <http://www.gnu.org/software/coreutils/>\nGeneral help using GNU software: <http://www.gnu.org/gethelp/>\nFor complete documentation, run: info coreutils 'wc invocation'"
			return outp
	flag_pool, file_pool = [],[]
	input_from_file = False
	fl=""
	tmp_flag = []
	was_arg = False
	for x in range(1, len(inp)):
		if inp[x].startswith('-'):
			if inp[x].startswith('--files0-from'):
				if inp[x] == '--files0-from':
					if x < len(inp)-1:
						input_from_file = True
						fl = inp[x+1]
						was_arg = True
					else:
						outp = "wc: option '--files0-from' requires an argument\n"
						outp += "Try 'wc --help' for more information."
						return outp
				elif inp[x].startswith('--files0-from='):
					input_from_file = True
					fl = inp[x][inp[x].find('=')+1:]
			else:
				tmp_flag.append(inp[x])
					
		else:
			if input_from_file and was_arg:
				was_arg=False
			elif input_from_file != was_arg:
				outp = "wc: extra operand '"+inp[x]+"'\n"+"file operands cannot be combined with --files0-from\n"
				outp += "Try 'wc --help' for more information."
				return outp
			
	if input_from_file:
		if fl != '-':	
			try:
				f = open(fl, 'r')
				infiles = f.read().split('\x00')
				inp = [inp[0]] + infiles + tmp_flag
				f.close()
			except IOError:
				return("wc: cannot open '"+ fl + "' for reading: No such file or directory")
		else:
			usr_inp_pool,opts = [], arg_parse([])
			while True:
				usr_inp = sys.stdin.readlines()
				usr_inp = ''.join(usr_inp);
				if usr_inp == '-':
					print("wc: when reading file names from stdin, no file name of '-' allowed"); 
					usr_inp_pool.append('loko'); continue
				if usr_inp == "":
					if len(usr_inp_pool) > 1:
						print(print_counts(opts[0],usr_inp_pool).split('\n')[-1])
					sys.exit()
				else:
					usr_inp_pool.append(usr_inp)
					opts = arg_parse(tmp_flag)
					res = print_counts(opts[0],[usr_inp])					
					print(res[:])
	
	double_dash = False
	d_dash_ind = 0

	for x in inp:
		if x.startswith('-'):
			if x == '-':
				file_pool.append(x)
			elif x == '--':
				double_dash = True; d_dash_ind = inp.index(x); break
			else:
				flag_pool.append(x)
		else:
			file_pool.append(x)
	if double_dash:
		flags_and_files = arg_parse(flag_pool+file_pool)
		if type(flags_and_files) is str:
			return flags_and_files
		tmp = flags_and_files[1] + inp[d_dash_ind+1:]
		return flags_and_files[0], tmp
	else:
		flags_and_files = arg_parse(flag_pool+file_pool)
		if type(flags_and_files) is str:
			return flags_and_files
		return flags_and_files[0], flags_and_files[1]


def print_counts(flags, files):

	"""
        This function creates a formatted wc-like message, depending on the file operands and
	count options.

        :param flags: A list of boolean values which contains count options
	:param files: a list which contains the file operands
        :return:  A wc-like formatted string with the counts specified
        """

	noFiles = False
	if len(files) == 0:
		files.append('-')
		noFiles = True

	total_count, largest_lines = [0,0,0,0,0],[]
	file_count = 0
	output = ""
	#counts = [line_count, word_count, char_count, byte_count]
	counts = [0,0,0,0,0]
	for fl in range(0,len(files)):
		inp= []
		file_count += 1
		if(files[fl] != '-'):
			try:
				f = open(files[fl], 'r')
				counts = counter(f.readlines(),False)
				f.close()
			except IOError:
				output += "wc: " + files[fl] + ": No such file or directory\n"
				continue
		else:
			if output != "":			
				print(output[:-1])			
			counts = counter(sys.stdin.readlines(),True)
			output=""
			
		for l in range(0,len(counts) - 1):
			total_count[l] += counts[l]
		
			
		largest_lines.append(counts[-1])
		total_count[-1] = max(largest_lines)
		str_pool = list(map(str, counts))

		for j in range(0,len(str_pool)):
			x = str_pool[j]
			if flags[j]:
				output += '\t' + x
		if noFiles:
			output += '\n'
		else:
			output += '\t' + files[fl] + '\n' 
		
		

	if file_count > 1:
		t_str_pool = list(map(str, total_count))
		for m in range(0,len(t_str_pool)):
			x = t_str_pool[m]
			if flags[m]:
				output += '\t' + x
		output += '\ttotal'
	else:
		output = output[:-1] 
	
	return output

##############################################################
def main():
	parsed_inp = arg_handling(sys.argv)
	if type(parsed_inp) is str:
		print(parsed_inp); sys.exit()
	out = print_counts(parsed_inp[0],parsed_inp[1])
	print(out)

if __name__ == "__main__":
	main()
