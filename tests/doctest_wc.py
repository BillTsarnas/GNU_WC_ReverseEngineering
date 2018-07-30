 # Everything is in a docstring!
"""
>>> import subprocess

--- Firstly, we check some possible flag combinations. An arbitrary number of
Flags can go in any order in the input arguments, before or after file names.

>>> subprocess.check_output('python3 wc.py testinputs/test.txt', shell=True)
b'\\t1\\t2680\\t34012\\ttestinputs/test.txt\\n'

>>> subprocess.check_output('python3 wc.py -w testinputs/test.txt -l', shell=True)
b'\\t1\\t2680\\ttestinputs/test.txt\\n'

--- Typing -wc should be the same as typing -w -c. A "flag/option" can have an
arbitrary, non zero number of characters w | l | c in any combination

>>> subprocess.check_output('python3 wc.py -wc testinputs/test.txt -l', shell=True)
b'\\t1\\t2680\\t34012\\ttestinputs/test.txt\\n'

>>> subprocess.check_output('python3 wc.py -wcwcwwcc testinputs/test.txt -llw', shell=True)
b'\\t1\\t2680\\t34012\\ttestinputs/test.txt\\n'

--- Here, we try putting wrong flags, like -o and -wlo. 'o' is not a valid option.

>>> subprocess.check_output('python3 wc.py -o testinputs/test.txt', shell=True)
b"wc: invalid option -- 'o'\\nTry 'wc --help' for more information.\\n"

>>> subprocess.check_output('python3 wc.py -o -k -n testinputs/test.txt', shell=True)
b"wc: invalid option -- 'o'\\nTry 'wc --help' for more information.\\n"

>>> subprocess.check_output('python3 wc.py -wlo testinputs/test.txt', shell=True)
b"wc: invalid option -- 'o'\\nTry 'wc --help' for more information.\\n"

--- Alternative flags, starting with '--' are not supported. The output is the same as wc's output for wrong alt flags
'--l','--w','--c' are only accepted

>>> subprocess.check_output('python3 wc.py --w testinputs/test.txt', shell=True)
b'\\t2680\\ttestinputs/test.txt\\n'

>>> subprocess.check_output('python3 wc.py --loko testinputs/test.txt', shell=True)
b"wc: unrecognized option '--loko'\\nTry 'wc --help' for more information.\\n"

--- Now, we take a look at multiple files (list of files)

>>> subprocess.check_output('python3 wc.py testinputs/test.txt testinputs/wc.py testinputs/empty.txt', shell=True)
b'\\t1\\t2680\\t34012\\ttestinputs/test.txt\\n\\t69\\t212\\t1760\\ttestinputs/wc.py\\n\\t0\\t0\\t0\\ttestinputs/empty.txt\\n\\t70\\t2892\\t35772\\ttotal\\n'

--- The same input file can be specified many times

>>> subprocess.check_output('python3 wc.py testinputs/chinese testinputs/chinese', shell=True)
b'\\t235\\t118\\t60607\\ttestinputs/chinese\\n\\t235\\t118\\t60607\\ttestinputs/chinese\\n\\t470\\t236\\t121214\\ttotal\\n'

--- Flags can be applied anywhere between the filepath arguments

>>> subprocess.check_output('python3 wc.py testinputs/test.txt -w testinputs/wc.py -l testinputs/armenian', shell=True)
b'\\t1\\t2680\\ttestinputs/test.txt\\n\\t69\\t212\\ttestinputs/wc.py\\n\\t1443\\t31978\\ttestinputs/armenian\\n\\t1513\\t34870\\ttotal\\n'

--- Some file names may point to missing files. Below, LifeOfBrian.py doen't exist in the testinputs directory

>>> subprocess.check_output('python3 wc.py testinputs/test.txt -w testinputs/LifeOfBrian.py testinputs/wc.py -l', shell=True)
b'\\t1\\t2680\\ttestinputs/test.txt\\nwc: testinputs/LifeOfBrian.py: No such file or directory\\n\\t69\\t212\\ttestinputs/wc.py\\n\\t70\\t2892\\ttotal\\n'

--- Here we check wc.py with no arguments: no options/flags and an empty file list. (STDIN mode is NOT supported)

>>> subprocess.check_output('python3 wc.py', shell=True)
b'wc: : No such file or directory\\n'

--- Finally, we check wc.py providing an empty file list, but flags are present

>>> subprocess.check_output('python3 wc.py -w -l', shell=True)
b'wc: : No such file or directory\\n'

--- Single double dash test case

>>> subprocess.check_output('python3 wc.py --', shell=True)
b'wc: --: No such file or directory\\n'

--- Multiple dashes test cases (dashes treated as missing files!)

>>> subprocess.check_output('python3 wc.py - -', shell=True)
b'wc: -: No such file or directory\\nwc: -: No such file or directory\\n\\t0\\t0\\t0\\ttotal\\n'

"""

 # We add the boilerplate to make this module both executable and importable.
if __name__ == "__main__":
	import doctest
	# The following command extracts all testable docstrings from the current module.
	doctest.testmod()
