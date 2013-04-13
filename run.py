#!/usr/bin/python 

import sys, re; 
import math as M; 
import random as R; 
import string as S; 

import dfa_description as DFADSC; 
import discrete_math as DISCRETE; 
import sequence_recognition as SEQR; 
import dfa_testing as DFAT; 
import data_io as DIO; 
import sequence_verification as SEQV; 

class run_test: 

	def __init__(self, student_id): 
		self.student_id = student_id; 
		self.curr_bench_dsc_name = ""; 
		self.curr_bench_dsc_names = [];

		self.curr_test_dsc_name = ""; 
		self.curr_test_dsctable = {}; 

		self.curr_scores = 0; 
		self.curr_single_score = 0; 
		self.curr_weights = 1; 
		self.fractional_score = 0.0; 

		self.curr_scores_table = {}; 
		self.curr_single_score_table = {}; 
		self.curr_weights_table = {}; 
		self.fractional_score_table = {}; 

	def curr_student_id(self): 
		return self.student_id; 

	def new_studnet_id(self, id): 
		self.student_id = id; 

	def assert_run(self, descriptor, condition):
		sys.stderr.write("RUN Exception: "+\
			str(descriptor)+'\t'+str(condition)+'\n'); 

	def err_run(self, descriptor, condition):
		sys.stderr.write("RUN irrecoverable ERROR: " \
			+ str(descriptor) + '\t' + str(condition)+'\n');
		sys.exit(0);

	## INPUT OUTPUT FUNCS ================================== ##

	def initialize_dfa_verif(self, name, sol_dir, test_dir): 
		self.dfav = SEQV.dfa_verification(name); 
		self.dfav.unset_notification(); 
		#self.dfav.import_benchdfa_definition(desc1); 
		self.dfav.set_test_dir(test_dir); 
		self.dfav.initialize_bench_dfaread(sol_dir); 
		self.dfav.initialize_execution(); 

	def change_verif_type(self, whether_continuous, continuous_type): 
		self.dfav.set_continuous(whether_continuous, continuous_type); 

	def sample_descriptions(self):  
		self.desc1 = DFADSC.form_desc1();
		self.err_desc1 = DFADSC.form_err_desc1();
		self.err_desc2 = DFADSC.form_err_desc2(); 	

	class randgen_params: 
		
		def __init__(self, length, bias, num_tests, default_score): 
			self.randgen_length = length; 
			self.randgen_bias = bias; 
			self.randgen_num_tests = num_tests; 
			self.randgen_default_score = default_score; 

	def parameterize_randgen(self, length, bias, \
	num_tests, default_score): 
		self.curr_randgen_params = self.randgen_params(length, bias, \
			num_tests, default_score); 

	def initialize_testing(self, randomness): 
		self.randomness = randomness; 
		if (not self.randomness): 
			self.dfav.initialize_prescribed_testing("curr_tests");
		elif (self.randomness == 1): 
			self.dfav.initialize_random_testing("curr_rand_tests", \
				self.randomness, self.curr_randgen_params); 
	#	sys.exit(0); 

		## ==================================== ## 

	## FOLLOWING 4 FUNCTIONS read individual scores/weights 
	## in various forms, after self.run_one(bench_name, dfa_description) 
	## is called with the appropriate solution (bench_name) 
	## and the desired student dfa description. 
	def read_scores(self): 
		return self.curr_scores; 

	def read_single_score(self): 
		return self.curr_single_score; 

	def read_weights(self): 
		return self.curr_weights; 

	def read_fractional_score(self): 
		return self.fractional_score; 

	## FOLLOWING 4 FUNCTIONS read grouped scores/weights 
	## in various forms, after 
	## self.run_several(dfa_description_table) 
	## which runs all the problems in the ./sol_DFAs directory 
	## along with a table of appropriate student dfa descriptions; 
	def lookup_scores(self, dsc_name): 
		return self.curr_scores_table[dsc_name]; 

	def lookup_single_score(self, dsc_name): 
		return self.curr_single_score_table[dsc_name]; 

	def lookup_weights(self, dsc_name): 
		return self.curr_weights_table[dsc_name]; 

	def lookup_fractional_score(self, dsc_name): 
		return self.fractional_score_table[dsc_name]; 

		## ==================================== ## 

	def import_curr_test_dsc(self, new_dsc): 
		self.curr_test_dsc_name = new_dsc; 

	def import_curr_test_dsctable(self, new_dsctbl): 
		self.curr_test_dsctable = new_dsctbl; 

	## EXECUTION FUNCTIONS ==================================== ## 

	def specify_bench_name(self, dsc_name): 
		self.curr_bench_dsc_name = dsc_name; 

	def specify_bench_names(self): 
		#print "BENCH NAMES:", self.dfav.present_bench_names(); 
		self.curr_bench_dsc_names = self.dfav.present_bench_names(); 

	def execute_one(self):  
		#self.dfav.initialize_testing(); 
		self.dfav.define_bench(self.curr_bench_dsc_name); 
	
		self.dfav.import_testdfa_definition(self.curr_test_dsc_name); 
		self.dfav.execute_n_compare(); 
		self.curr_scores, self.curr_single_score, self.curr_weights = \
			self.dfav.present_scoring(); 

	def fraction_score(self): 
		potential = 0; 
		for weight in self.curr_weights: 
			potential += weight; 
		self.fractional_score = \
			(float(self.curr_single_score) / float(potential));

	def execute_tests(self):
		print self.curr_test_dsctable; 
		if (len(self.curr_test_dsctable.keys()) \
		!= len(self.curr_bench_dsc_names)): 
			self.err_run("# TEST DFAs does not match # SOLUTIONS", \
				str(len(self.curr_test_dsctable)) + ':' \
				+ str(len(self.curr_bench_dsc_names))); 
		for i in range(0, len(self.curr_bench_dsc_names), 1): 
			curr_bench_name = self.curr_bench_dsc_names[i]; 
			self.specify_bench_name(curr_bench_name); 
			self.import_curr_test_dsc(\
				self.curr_test_dsctable[curr_bench_name]); 
			self.execute_one(); 
			self.fraction_score(); 
			self.curr_scores_table[curr_bench_name] = self.curr_scores; 
			self.curr_single_score_table[curr_bench_name] = \
				self.curr_single_score; 
			self.curr_weights_table[curr_bench_name] = self.curr_weights; 
			self.fractional_score_table[curr_bench_name] = \
				self.fractional_score; 

	def run_one(self, bench_name, new_dsc): 
		self.specify_bench_name(bench_name); 
		self.import_curr_test_dsc(new_dsc); 
		self.execute_one(); 
		self.fraction_score(); 

	def run_several(self, new_dsctbl): 
		self.import_curr_test_dsctable(new_dsctbl); 
		self.specify_bench_names(0); 
		self.execute_tests(); 

	## TEST FUNCS ========================================= ##

	def test1_verification(self): 
		#self.dfav.initialize_testing("tmp1"); 
		self.dfav.define_bench(self.curr_bench_dsc_name); 
	
		self.dfav.import_testdfa_definition(self.desc1); 
		self.dfav.execute_n_compare(); 

	def test2_verification(self): 
		#self.dfav.initialize_testing("tmp1"); 
		for dfa_name in self.curr_bench_dsc_names: 
			self.dfav.define_bench(dfa_name); 	
			self.dfav.import_testdfa_definition(self.desc1); 
			self.dfav.execute_n_compare(); 

def test_run(): 
	newrt = run_test("course_staff"); 
	newrt.initialize_dfa_verif( "dfaver1", "./test_cases/"); 
	newrt.initialize_testing(0); 

	desc1 = DFADSC.form_desc1();
	err_desc1 = DFADSC.form_err_desc1();
	err_desc2 = DFADSC.form_err_desc2(); 	

	newrt.sample_descriptions(); 
	newrt.specify_bench_name('sandy bridge'); 
	newrt.specify_bench_names(); 
	#newrt.test1_verification(); 
	#newrt.test2_verification(); 

	newrt.import_curr_test_dsc(desc1); 
	newrt.specify_bench_name('ivy bridge'); 
	newrt.execute_one(); 

	print '-|'*36;
	new_dsc_tbl = {"sandy bridge":err_desc1, "ivy bridge":err_desc2}; 
	newrt.import_curr_test_dsctable(new_dsc_tbl); 
	newrt.specify_bench_names(); 
	newrt.execute_tests(); 

#test_run(); 

def main(student_id, whether_continuous, continuous_type, \
solutions_dir, tests_dir, randomization): 
	runtestx = run_test(student_id); 
	runtestx.initialize_dfa_verif( \
		student_id, solutions_dir, tests_dir); 
	runtestx.change_verif_type(whether_continuous, continuous_type); 
	if (randomization): 
		runtestx.parameterize_randgen(20, 0, 10, 1.0); 
	runtestx.initialize_testing(randomization); 
	runtestx.specify_bench_names(); 
	if (student_id == "course_staff"): 
		desc1 = DFADSC.form_desc1();
		desc2 = DFADSC.form_desc2(); 
		err_desc1 = DFADSC.form_err_desc1();
		err_desc2 = DFADSC.form_err_desc2(); 	
		
		new_dsc_tbl = {"DFA001":desc1, "DFA1010":desc2, \
			"DFA0101":err_desc1, "DFA0011":err_desc2}; 
		runtestx.import_curr_test_dsctable(new_dsc_tbl); 
		runtestx.specify_bench_names(); 
		runtestx.execute_tests(); 
	return runtestx; 

## use the instance runtestx , which is set up in main(); 
## use run_one() or run_several() depending on mode of input 
## (either individual student dfa designs or 
## a table of all dfas from a particular student); 
runtestx = main("course_staff", 1, 1, \
	"./sol_DFA_group1/", "./test_cases_group1/", 1);

