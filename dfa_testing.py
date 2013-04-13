#!/usr/bin/python 

import sys, re; 
import math as M; 
import random as R; 
import string as S; 

import data_io as DIO; 
import test_generation as GENT; 

## BEGIN TEST CLASS ===================
## ===================================> 

class dfa_tests: 

	def __init__(self, name): 
		self.name = name; 
		self.test_files = []; 
		self.test_dir = "./"; 
		self.curr_test_file = ""; 

		self.test_len_parameter = 0; 
		self.test_lines = []; 

		self.legal_symbols = []; 
		self.legal_states = []; 
		self.tests = {}; 

	def set_test_directory(self, new_dir): 
		self.test_dir = new_dir;  

	def set_len_parameter(self, new_len): 
		self.test_len_parameter = new_len; 

	def set_legal_symbols(self, symbols): 
		self.legal_symbols = symbols; 

	def set_legal_states(self, states): 
		self.legal_states = states; 

	def assert_tst(self, descriptor, condition):
		sys.stderr.write("TEST Exception: "+\
			str(descriptor)+'\t'+str(condition)+'\n'); 

	def err_tst(self, descriptor, condition):
		sys.stderr.write("TEST irrecoverable ERROR: " \
			+ str(descriptor) + '\t' + str(condition)+'\n');
		sys.exit(0);

	## TEST SETUP FUNCTIONS ================================ ## 

	def set_test_dir(self, new_dir): 
		self.test_dir = new_dir; 
		if (self.test_dir.strip() != "./"): 
			self.test_dir_set = 1; 
		self.candidate_files = DIO.get_files_x(self.test_dir); 

	def symcheck_test_line(self, line): 
		passed = 1; 
		for lit in line: 
			if (lit not in self.legal_symbols): 
				passed = 0; 
				self.err_tst("TEST CHAR not a legal symbol in ", lit); 
		return passed; 

	def baseline_symcheck_test_line(self, line): 
		passed = 1; 
		if (not DIO.regex_alphanum.match(line)): 
			passed = 0; 
			self.err_tst("TEST CHAR not a legal symbol in ", line); 
		return passed; 

	def read_test_file(self): 
		curr_test = {}; 
		lines = DIO.read_file(self.curr_test_file); 
		test_name = lines[0].strip(); 
		for line in lines[1:len(lines)]: 
			words = line.strip().split(); 
			if (len(words) != 4): 
				self.assert_tst("TEST ENTRY FORMAT INCORRECT", len(words));
				continue; 
			name = words[0]; 
			try: 
				score = int(words[1]); 
			except: 
				self.assert_tst("TEST SCORE FORMAT INCORRECT", score);
				continue; 
			start = words[2]; 
			if (not self.baseline_symcheck_test_line(words[3])): 
				self.assert_tst("TEST SYMBOL FORMAT INCORRECT", score);
				continue; 
			curr_test[name] = (words[3], score, start); 
		print test_name, curr_test; 
		self.tests[test_name] = curr_test; 

	def read_test_files(self): 
		self.test_files = DIO.get_files_x(self.test_dir); 
		self.tests = {}; 
		for tfile in self.test_files: 
			self.curr_test_file = tfile; 
			self.read_test_file(); 

	def show_tests(self): 
		for tname in self.tests: 
			print "DFA NAME:", tname; 
			for entry in self.tests[tname]: 
				print '\t', entry, "test_string:", \
					self.tests[tname][entry][0], "max_score:", \
					self.tests[tname][entry][1], "start_state:", \
					self.tests[tname][entry][2]; 
		sys.exit(0); 

	## RANDOM GENERATION =============================== ## 

	def setup_randgen_nonbin(self, length, symbol_dict, \
	 num_tests, default_score): 
		self.randgen = GENT.random_test(); 
		self.randgen.set_symbols(symbol_dict, 0); 
		self.randgen.set_parameters(length, 0); 
		self.randgen_cnt = num_tests; 
		self.randgen_score = default_score; 

	def setup_randgen_bin(self, length, bias, num_tests, default_score): 
		self.randgen = GENT.random_test(); 
		self.randgen.set_symbols({}, 1); 
		self.randgen.set_parameters(length, bias); 
		self.randgen_cnt = num_tests; 
		self.randgen_score = default_score; 

	def random_test_case(self, test_name): 
		curr_test = {};
		name_base = "randtest";  
		default_start = 'x'; 
		test_cnt = 0; 
		curr_test_cases = self.randgen.gen(self.randgen_cnt); 
		for test_case in curr_test_cases: 
			curr_test[name_base+str(test_cnt)] = \
				(test_case, self.randgen_score, default_start); 
			test_cnt += 1; 
		self.tests[test_name] = curr_test; 

	def random_test_cases(self, dfa_names): 
		self.tests = {}; 
		for name in dfa_names: 
			self.random_test_case(name); 

	## ADAPTIVE GENERATION ================================= ## 

	def setup_adaptive_bin(self, whether_continuous, length, \
	outcome_bias, num_tests, default_score): 
		self.adaptive = GENT.adaptive_test(); 
		self.adaptive.initialize_exe( \
			whether_continuous, outcome_bias, default_score); 
		self.adaptive.set_symbols({}, 1); 
		self.adaptive.set_parameters(length, outcome_bias); 

	def adaptive_test_cases(self, selection_width, adapt_cnt): 
		name_cnt = 0; 
		for index in range(0, num_tests, 1): 
			new_name = "adapttest"+str(index); 
			self.tests[new_name] = \
				self.adaptive.adapt(selection_width, adapt_cnt); 

	def check_dfa_legality(self, dfa_name):
		for entry in self.tests[dfa_name]: 
			if (not self.symcheck_test_line(\
			self.tests[dfa_name][entry][0])): 
				self.assert_tst("SYMBOL ILLEGAL", \
					self.tests[dfa_name][entry][0]); 
			if ((self.tests[dfa_name][entry][2] not in self.legal_states) \
			and (self.tests[dfa_name][entry][2].strip() != 'x')): 
				self.err_tst("START STATE ILLEGAL:", \
					self.tests[dfa_name][entry][2]); 

	def present_test(self, dfa_name):
		if (dfa_name not in self.tests.keys()): 
			self.err_tst("NO TEST EXIST FOR DFA:", dfa_name);  
		self.check_dfa_legality(dfa_name); 
		return self.tests[dfa_name]; 

## END TEST CLASS ===================
## <=================================

