import unittest
import subprocess
from wc import arg_handling, print_counts, counter

class ArgTest(unittest.TestCase):
	
	#input: List of input arguments
	#output: ([line_enable,word_enable,byte_enable], List of Files)
	def test_no_flags(self):
		self.assertEqual(arg_handling(['wc.py', 'file']),([True,True,True],['file']))
	def test_all_flags(self):
		self.assertEqual(arg_handling(['wc.py','-l', '-c', '-w', 'file']),([True,True,True],['file']))	
	def test_all_flags1(self):
		self.assertEqual(arg_handling(['wc.py','--l', '-wwc', 'file']),([True,True,True],['file']))
	def test_one_flag(self):
		self.assertEqual(arg_handling(['wc.py', 'file', '-l']),([True,False,False],['file']))
	def test_two_flags(self):
		self.assertEqual(arg_handling(['wc.py', 'file', '-l', '-c']),([True,False,True],['file']))
	
	def test_no_input_file(self):
		self.assertEqual(arg_handling(['wc.py',]), "wc: : No such file or directory")
	def test_no_input_file_flags(self):
		self.assertEqual(arg_handling(['wc.py', '-l']), "wc: : No such file or directory")

	def test_mul_files_all_flags(self):
		self.assertEqual(arg_handling(['wc.py', 'file1', 'file2']),([True,True,True],['file1', 'file2']))
	def test_mul_files_flags(self):
		self.assertEqual(arg_handling(['wc.py', '-w','file1','-l','file2']),([True,True,False],['file1', 'file2']))
	def test_mul_dashes(self):
		self.assertEqual(arg_handling(['wc.py', '-w','-','-l','-']),([True,True,False],['-', '-']))

	def test_double_dash(self):
		self.assertEqual(arg_handling(['wc.py', '-w','--','-l']),"wc: --: No such file or directory")
	def test_wrongflag1(self):
		self.assertEqual(arg_handling(['wc.py', '-w','-o','file']),"wc: invalid option -- 'o'\nTry 'wc --help' for more information.")
	def test_wrongflag2(self):
		self.assertEqual(arg_handling(['wc.py', '-wlo','file']),"wc: invalid option -- 'o'\nTry 'wc --help' for more information.")
	def test_wrongflag3(self):
		self.assertEqual(arg_handling(['wc.py', '--loko']),"wc: unrecognized option '--loko'\nTry 'wc --help' for more information.")

class CountTest(unittest.TestCase):
	
	def test_ascii(self):
		tested = counter(open('testinputs/wc.py','r'))
		expected = (106,344,2927)
		self.assertEqual(tested,expected)
	def test_greek(self):
		tested = counter(open('testinputs/test.txt','r'))
		expected = (1,2680,34012)
		self.assertEqual(tested,expected)
	def test_chinese(self):
		tested = counter(open('testinputs/chinese','r'))
		expected = (235,118,60607)
		self.assertEqual(tested,expected)
	def test_armenian(self):
		tested = counter(open('testinputs/armenian','r'))
		expected = (1443,31978,396307)
		self.assertEqual(tested,expected)
	def test_empty(self):
		tested = counter(open('testinputs/empty.txt','r'))
		expected = (0,0,0)
		self.assertEqual(tested,expected)
	

class PrintCountsTest(unittest.TestCase):

	def test_all_flags(self):
		tested = print_counts([True,True,True],['testinputs/test.txt']).split()
		expected = subprocess.check_output('wc testinputs/test.txt', shell=True).decode('utf-8').split()
		self.assertEqual(tested,expected)	
	def test_one_flag(self):
		tested = print_counts([True,False,False],['testinputs/test.txt']).split()
		expected = subprocess.check_output('wc -l testinputs/test.txt', shell=True).decode('utf-8').split()
		self.assertEqual(tested,expected)
	def test_two_flags(self):
		tested = print_counts([True,False,True],['testinputs/test.txt']).split()
		expected = subprocess.check_output('wc -l -c testinputs/test.txt', shell=True).decode('utf-8').split()
		self.assertEqual(tested,expected)
	#no input file test case is handled by arg_handling
	
	def test_mul_files_all_flags(self):
		tested = print_counts([True,True,True],['testinputs/test.txt','testinputs/chinese']).split()
		expected = subprocess.check_output('wc testinputs/test.txt testinputs/chinese', shell=True).decode('utf-8').split()
		self.assertEqual(tested,expected)
	def test_mul_files_flags(self):
		tested = print_counts([True,True,False],['testinputs/test.txt','testinputs/empty.txt','testinputs/chinese']).split()
		expected = subprocess.check_output('wc -w -l testinputs/test.txt testinputs/empty.txt testinputs/chinese', shell=True).decode('utf-8').split()
		self.assertEqual(tested,expected)

	#For these test cases, we compare the output of print_counts() with the raw wc expected output
	#The real wc quits with an error code 2 (for these cases) and subprocess.check_output can't have that
	def test_mul_dashes(self):
		tested = print_counts([True,True,False],['-','-'])
		expected = "wc: -: No such file or directory\nwc: -: No such file or directory\n\t0\t0\ttotal"
		self.assertEqual(tested,expected)
	def test_mul_files_one_missing(self):
		tested = print_counts([True,True,True],['testinputs/armenian','ducks'])
		expected = "\t1443\t31978\t396307\ttestinputs/armenian\nwc: ducks: No such file or directory\n\t1443\t31978\t396307\ttotal"
		self.assertEqual(tested,expected)
	def test_one_file_missing(self):
		tested = print_counts([True,True,True],['ducks'])
		expected = "wc: ducks: No such file or directory"
		self.assertEqual(tested,expected)	
	

if __name__ == '__main__':
	unittest.main()
