import sys
import os
from collections import defaultdict
lib_path = '/'.join(os.path.abspath(__file__).split('/')[0:-2])
sys.path.append(lib_path+'/utils/')
sys.path.append(lib_path)
import SpliceGraph as sg
import PlottedGraph as pg
from utils import *
from plotting_tools import * 

class TestUtils(object):
	def test_process_abundance_file(self):
		file = 'input_files/test_abundance.tsv'
		df = process_abundance_file(file, ['count_1a', 'count_2a'])

		print(df)
		
		test_pairs = df.apply(lambda x: (x.tid, x.counts), axis=1)
		control_pairs = ((0,3),(1,7),(2,11))
		print('test pairs')
		print(test_pairs)
		check_pairs(control_pairs, test_pairs)

def check_pairs(control, test):
	print('control')
	print(control)
	for t in test:
		print(t)
		assert t in control