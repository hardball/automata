#!/usr/bin/python 

import sys, re; 
import math as M; 
import random as R; 
import string as S; 

import dfa_description as DFADSC; 
import discrete_math as DISCRETE; 
import sequence_recognition as SEQR; 
import dfa_testing as DFAT; 
import dfa_execution as DFAEXE; 
import data_io as DIO; 

## BEGIN DFAVER CLASS ==================
## ====================================>

class dfa_verification: 

	def __init__(self, name): 
		self.name = name; 
		self.notify = 0; 
		self.dfaread = {}; 
		self.dfaread_names = []; 
	
		self.err_log = []; 
		self.err_log_aug = {}; 

		self.testing = ""; 
		self.test_dir = "./"; 
		self.test_dir_set = 0; 
		self.candidate_files = []; 
		#self.test_file = "testx.txt"; 

		self.curr_test = {}; 
		self.curr_sigma = []; 
		self.bench_dfa_desc = ""; 
		self.test_dfa_desc = ""; 

		self.bench_dfa = {}; 
		self.test_dfa = {}; 

		self.execution = {}; 
		self.reset_execution(); 

		self.randomness = 0; 

	def reset_execution(self): 
		self.bench_dfa_acceptances = []; 
		self.test_dfa_acceptances = []; 
		self.bench_dfa_acceptance_sequence = []; 
		self.test_dfa_acceptance_sequence = []; 

		self.curr_results = []; 
		self.curr_weights = []; 
		self.curr_scores = []; 
		self.single_score = 0; 

		self.whether_continuous = 0; 
		self.curr_result_sequence = []; 
		self.sequence_comparison_type = 0; 

	## CLASS UTILITY FUNCTION ================================ ## 

	def set_notification(self): 
		self.notify = 1; 

	def unset_notification(self): 
		self.notify = 0; 

	def set_continuous(self, seq, seqtype): 
		self.whether_continuous = seq; 
		self.sequence_comparison_type = seqtype; 

	def assert_dfav(self, descriptor, condition):
		if (self.notify):
			sys.stderr.write("DFAV Exception: "+\
				str(descriptor)+'\t'+str(condition)+'\n'); 

	def err_dfav(self, descriptor, condition):
		if (1 or self.notify):
			sys.stderr.write("DFAV irrecoverable ERROR: " \
				+ str(descriptor) + '\t' + str(condition)+'\n');
		sys.exit(0);

	def err_dfav_list(self, descriptor, condition, err_list):
		if (1 or self.notify):
			sys.stderr.write("DFAV irrecoverable ERROR: " \
				+ str(descriptor) + '\t' + str(condition)+'\n');
			print err_list; 
		sys.exit(0);

	def clear_err_log(self): 
		self.err_log = []; 
		self.err_log_aug = {};  

	def log_dfav(self, descriptor, condition):
		err_line = "DFAV irrecoverable ERROR: " \
			+ str(descriptor) + '\t' + str(condition)+'\n';
		if (self.notify): 
			sys.stderr.write(err_line); 
		self.err_log.append(err_line); 

	def log_dfav_list(self, descriptor, condition, err_list):
		err_line = "DFAV irrecoverable ERROR: " \
			+ str(descriptor) + '\t' + str(condition)+'\n';
		if (self.notify): 
			sys.stderr.write(err_line); 
		self.err_log.append(err_line); 
		if (err_line not in self.err_log_aug): 
			self.err_log_aug[err_line] = []; 
			self.err_log_aug[err_line].append(err_list); 
		else: 
			self.err_log_aug[err_line].append(err_list); 

	def show_log(self): 
		print "\nDFAV", self.name, "ERRORS:"; 
		for entry in self.err_log: 
			print entry.strip(); 
			if (entry in self.err_log_aug): 
				print '\t', self.err_log_aug[entry]; 
		print 'END LOG....\n'; 

	## DFA INITIALIZATION AND SETUP ========================== ##

	def set_testbench(self, bench_dfa): 
		self.bench_dfa = bench_dfa; 

	def import_testdfa_definition(self, new_dfa_def):  
		self.test_dfa_desc = new_dfa_def; 
		self.initialize_test_dfa(); 

	def import_benchdfa_definition(self, bench_dfa_desc): 
		self.bench_dfa_desc = bench_dfa_desc; 
		self.initialize_bench_dfa(); 

	def initialize_test_dfa(self): 
		self.test_dfa = SEQR.deterministic_finite_state_automaton(""); 
		if (self.notify): 
			self.test_dfa.set_notification(); 
		else: 
			self.test_dfa.unset_notification(); 
		self.test_dfa.import_desc(self.test_dfa_desc); 
		self.test_dfa.check_desc_isDFA();   
		self.test_dfa.check_desc_DFA_nontrivial(); 
		self.test_dfa.show_log(); 

	def initialize_bench_dfa(self): 
		self.bench_dfa = SEQR.deterministic_finite_state_automaton(""); 
		if (self.notify): 
			self.bench_dfa.set_notification(); 
		else: 
			self.bench_dfa.unset_notification(); 
		self.bench_dfa.import_desc(self.bench_dfa_desc); 
		self.bench_dfa.check_desc_isDFA();   
		self.bench_dfa.check_desc_DFA_nontrivial(); 
		self.bench_dfa.show_log(); 

	def initialize_bench_dfaread(self, directory): 
		self.dfaread = DFADSC.DFA_descript_read(); 
		self.dfaread.unset_notification(); 
		self.dfaread.set_dir(directory); 
		self.dfaread.parse_xmls(); 
		self.dfaread.translate(); 
		self.dfaread_names = self.dfaread.present_dfa_names(); 

	def present_bench_names(self): 
		return self.dfaread_names; 

	def initialize_execution(self): 
		self.execution = DFAEXE.dfa_execution(); 

	## BENCH/TEST SETUP FUNCTIONS ================================ ## 

	def initialize_prescribed_testing(self, name): 
		self.randomness = 0; 
		self.testing = DFAT.dfa_tests(name); 
		if (self.test_dir_set): 
			self.testing.set_test_directory(self.test_dir); 
		else: 
			self.err_dfav("DIRECTORY FOMAT INCORRECT:", self.test_dir);
		self.testing.read_test_files(); 
		self.testing.show_tests(); 

	def initialize_random_testing(self, name, random_type, randgen_params): 
		self.randomness = random_type; 
		self.testing = DFAT.dfa_tests(name); 
		self.testing.setup_randgen_bin(randgen_params.randgen_length, \
			randgen_params.randgen_bias, randgen_params.randgen_num_tests, \
			randgen_params.randgen_default_score); 
		self.testing.random_test_cases(self.dfaread_names); 

	def set_test_dir(self, new_dir): 
		self.test_dir = new_dir; 
		if (self.test_dir.strip() != "./"): 
			self.test_dir_set = 1; 
		self.candidate_files = DIO.get_files_x(self.test_dir); 

	def define_bench(self, bench_desc_name): 
		self.bench_dfa_desc = \
			self.dfaread.present_dfa_descript(bench_desc_name); 
		self.curr_sigma = self.bench_dfa_desc.present_symbols();
		self.testing.set_legal_symbols(self.curr_sigma); 
		self.testing.set_legal_states(self.bench_dfa_desc.present_states());
		self.curr_test = self.testing.present_test(bench_desc_name);
		self.initialize_bench_dfa(); 

	def new_test_dfa(self, test_desc): 
		self.test_dfa_desc = test_desc; 
	
	## TEST EXECUTION FUNCTIONS ============================ ## 

	def execute_bench_dfa(self): 
		self.execution.import_components(self.bench_dfa.present_delta(), \
			self.bench_dfa.present_finals(), \
			self.bench_dfa.present_initial()); 
		self.execution.import_test(self.curr_test); 
		self.bench_dfa_acceptances = self.execution.execute_test(); 
		self.curr_weights = self.execution.present_curr_weights(); 
	
	def execute_test_dfa(self): 
		self.execution.import_components(self.test_dfa.present_delta(), \
			self.test_dfa.present_finals(), \
			self.test_dfa.present_initial()); 
		self.execution.import_test(self.curr_test); 
		self.test_dfa_acceptances = self.execution.execute_test(); 
		self.curr_weights = self.execution.present_curr_weights(); 

	def compare_acceptances(self): 
		self.curr_results = []; 
		if (1 or self.notify): 
			print "BENCH:", self.bench_dfa_acceptances; 
			print "XTEST:", self.test_dfa_acceptances; 
		if (len(self.bench_dfa_acceptances) != \
		len(self.test_dfa_acceptances)): 
			self.err_dfav("TESTING PROCEDURE went wrong", ":-("); 
		for i in range(0, len(self.bench_dfa_acceptances), 1): 
			if (self.bench_dfa_acceptances[i] == \
			self.test_dfa_acceptances[i]): 
				score = 1; 
			else: 
				score = 0; 
			self.curr_results.append(score); 
		if (1 or self.notify): 
			print "RESULTS:", self.curr_results; 

	def compute_scores(self): 
		self.curr_scores = []; 
		self.single_score = 0; 
		for i in range(0, len(self.curr_results), 1): 
			score = self.curr_results[i] * self.curr_weights[i]; 
			self.curr_scores.append(score); 
			self.single_score += score; 
		print "SCORES:", self.curr_scores; 
		print "MAXIMA:", self.curr_weights; 
		print "SUM SCORES:", self.single_score; 

	def execute_n_compare_end(self): 
		self.execute_bench_dfa(); 
		self.execute_test_dfa(); 	
		self.compare_acceptances(); 
		self.compute_scores(); 

	def present_scoring(self): 
		return (self.curr_scores, self.single_score, self.curr_weights); 

	def execute_bench_dfa_continuous(self): 
		self.execution.import_components(self.bench_dfa.present_delta(), \
			self.bench_dfa.present_finals(), \
			self.bench_dfa.present_initial()); 
		self.execution.import_test(self.curr_test); 
		self.bench_dfa_acceptance_sequence = \
			self.execution.execute_test_continuous(); 
		self.curr_weights = self.execution.present_curr_weights(); 
	
	def execute_test_dfa_continuous(self): 
		self.execution.import_components(self.test_dfa.present_delta(), \
			self.test_dfa.present_finals(), \
			self.test_dfa.present_initial()); 
		self.execution.import_test(self.curr_test); 
		self.test_dfa_acceptance_sequence = \
			self.execution.execute_test_continuous(); 

	def sequence_comparison(self, seq1, seq2): 
		#print "SEQ CMP TYPE:", self.name, self.sequence_comparison_type; 
		if (not self.sequence_comparison_type): 
			return float(seq1 == seq2);  
		else: 
			score = 0.0; 
			for index in range(0, len(seq1), 1): 
				if (seq1[index] == seq2[index]): 
					score += 1.0; 
				else: 
					score += 0.0; 
			return (score / float(len(seq1))); 

	def compare_acceptances_continuous(self): 
		self.curr_result_sequence = []; 
		if (1 or self.notify): 
			print "BENCHSEQ:", self.bench_dfa_acceptance_sequence; 
			print "XTESTSEQ:", self.test_dfa_acceptance_sequence; 
		if (len(self.bench_dfa_acceptance_sequence) != \
		len(self.test_dfa_acceptance_sequence)): 
			self.err_dfav("TESTING PROCEDURE went wrong", ":-("); 
		for i in range(0, len(self.bench_dfa_acceptance_sequence), 1): 
			score = self.sequence_comparison( \
				self.bench_dfa_acceptance_sequence[i], \
				self.test_dfa_acceptance_sequence[i]); 
			self.curr_result_sequence.append(score); 
		if (1 or self.notify): 
			print "RESULTSEQ:", self.curr_result_sequence; 

	def compute_scores_continuous(self): 
		self.curr_scores = []; 
		self.single_score = 0; 
		for i in range(0, len(self.curr_result_sequence), 1): 
			score = self.curr_result_sequence[i] \
				* float(self.curr_weights[i]); 
			self.curr_scores.append(score); 
			self.single_score += score; 
		print "SCORES:", self.curr_scores; 
		print "MAXIMA:", self.curr_weights; 
		print "SUM SCORES:", self.single_score; 

	def execute_n_compare_continuous(self): 
		self.execute_bench_dfa_continuous(); 
		self.execute_test_dfa_continuous(); 	
		self.compare_acceptances_continuous(); 
		self.compute_scores_continuous(); 

	def execute_n_compare(self): 
		if (not self.whether_continuous): 
			self.execute_n_compare_end(); 
		else: 
			self.execute_n_compare_continuous(); 

## <===================================>
## END DFAVER CLASS ===================;

