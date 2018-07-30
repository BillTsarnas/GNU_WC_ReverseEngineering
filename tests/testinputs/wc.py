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

def counter( f ):
	num_lines, num_words, num_bytes = 0,0,0
	for line in f:
		num_lines += 1
		num_words += len(line.split())
		num_bytes += len(line.encode('utf-8'))
	f.close()
	return num_lines, num_words, num_bytes


def arg_handling( inp ):
	parser = WcParser()
	parser.add_argument("-l", "--lines", action="store_true",help="print the newline counts")
	parser.add_argument("-w", "--words", action="store_true",help="print the word counts")
	parser.add_argument("-c", "--bytes", action="store_true",help="print the byte counts")
	parser.add_argument("files", help="input files", nargs="*")
	#Argparse takes only the flags, then the file names
	flag_pool, file_pool = [],[]
	for x in inp:
		if x.startswith('-'):
			if x == '--':
				return 'wc: --: No such file or directory'
			if x != '-':
				flag_pool.append(x)
			else:
				file_pool.append(x)
		else:
			file_pool.append(x)

	try:	
		args = parser.parse_args(list(reversed(flag_pool)) + file_pool)
	except ValueError as e:
		return str(e)

	flags = [args.lines, args.words, args.bytes]

	if len(args.files) == 1:
		return 	'wc: : No such file or directory'
	
	if args.lines == False and args.words == False and args.bytes == False:
		flags = [True,True,True]
	
	files=args.files[1:]

	return flags, files


def print_counts(flags, files):
	total_count = [0,0,0]
	file_count = 0
	output = ""
	for fl in range(0,len(files)):
		try:
			file_count += 1
			f = open(files[fl], 'r')
			#counts = [line_count, word_count, byte_count]
			counts = [0,0,0]
			counts = counter(f)

			for l in range(0,len(counts)):
				total_count[l] += counts[l]
			str_pool = list(map(str, counts))
			for j in range(0,len(str_pool)):
				x = str_pool[j]
				if flags[j]:
					output += '\t' + x
			output += '\t' + files[fl] + '\n' 
		except IOError:
			output += "wc: " + files[fl] + ": No such file or directory\n"

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
