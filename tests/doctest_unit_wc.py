 # Everything is in a docstring!
"""
>>> import subprocess
>>> from wc import arg_handling, print_counts, counter

------------------- arg_handling TEST CASES-------------------------------------

>>> arg_handling(['wc.py', 'file'])
([True, True, True], ['file'])

>>> arg_handling(['wc.py','-l', '-c', '-w', 'file'])
([True, True, True], ['file'])

>>> arg_handling(['wc.py','--l', '-wwc', 'file'])
([True, True, True], ['file'])

>>> arg_handling(['wc.py', 'file', '-l'])
([True, False, False], ['file'])

>>> arg_handling(['wc.py', 'file', '-l', '-c'])
([True, False, True], ['file'])

>>> arg_handling(['wc.py',])
'wc: : No such file or directory'

>>> arg_handling(['wc.py', '-l'])
'wc: : No such file or directory'

>>> arg_handling(['wc.py', 'file1', 'file2'])
([True, True, True], ['file1', 'file2'])

>>> arg_handling(['wc.py', '-w','file1','-l','file2'])
([True, True, False], ['file1', 'file2'])

>>> arg_handling(['wc.py', '-w','-','-l','-'])
([True, True, False], ['-', '-'])

>>> arg_handling(['wc.py', '-w','--','-l'])
'wc: --: No such file or directory'

>>> arg_handling(['wc.py', '-w','-o','file'])
"wc: invalid option -- 'o'\\nTry 'wc --help' for more information."

>>> arg_handling(['wc.py', '-wlo','file'])
"wc: invalid option -- 'o'\\nTry 'wc --help' for more information."

>>> arg_handling(['wc.py', '--loko'])
"wc: unrecognized option '--loko'\\nTry 'wc --help' for more information."


------------------- counter TEST CASES-------------------------------------

>>> counter(open('testinputs/wc.py','r'))
(106, 344, 2927)

>>> counter(open('testinputs/test.txt','r'))
(1, 2680, 34012)

>>> counter(open('testinputs/chinese','r'))
(235, 118, 60607)

>>> counter(open('testinputs/armenian','r'))
(1443, 31978, 396307)

>> counter(open('testinputs/empty.txt','r'))
(0, 0, 0)

------------------- print_counts TEST CASES-------------------------------------

>>> print_counts([True,True,True],['testinputs/test.txt'])
'\\t1\\t2680\\t34012\\ttestinputs/test.txt'

>>> print_counts([True,False,False],['testinputs/test.txt'])
'\\t1\\ttestinputs/test.txt'

>>> print_counts([True,False,True],['testinputs/test.txt'])
'\\t1\\t34012\\ttestinputs/test.txt'

>>> print_counts([True,True,True],['testinputs/test.txt','testinputs/chinese'])
'\\t1\\t2680\\t34012\\ttestinputs/test.txt\\n\\t235\\t118\\t60607\\ttestinputs/chinese\\n\\t236\\t2798\\t94619\\ttotal'

>>> print_counts([True,True,False],['testinputs/test.txt','testinputs/empty.txt','testinputs/chinese'])
'\\t1\\t2680\\ttestinputs/test.txt\\n\\t0\\t0\\ttestinputs/empty.txt\\n\\t235\\t118\\ttestinputs/chinese\\n\\t236\\t2798\\ttotal'

>>> print_counts([True,True,False],['-','-'])
'wc: -: No such file or directory\\nwc: -: No such file or directory\\n\\t0\\t0\\ttotal'

>>> print_counts([True,True,True],['testinputs/armenian','ducks'])
'\\t1443\\t31978\\t396307\\ttestinputs/armenian\\nwc: ducks: No such file or directory\\n\\t1443\\t31978\\t396307\\ttotal'

>>> print_counts([True,True,True],['ducks'])
'wc: ducks: No such file or directory'

"""

 # We add the boilerplate to make this module both executable and importable.
if __name__ == "__main__":
	import doctest
	# The following command extracts all testable docstrings from the current module.
	doctest.testmod()
