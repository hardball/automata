#!/usr/bin/python

import sys, re; 
import math as M; 
import random as R; 
import string as S; 

import dfa_description as DFADSC; 
import discrete_math as DISCRETE; 

## BEGIN DFSA CLASS ==================
## ==================================>

class deterministic_finite_state_automaton: 

	def __init__(self, name): 
		self.name = name; 
		self.notify = 0; 
		self.dfa_descript = {}; 

		self.curr_state = ""; 
		self.reacheable = {}; 

		self.err_log = []; 
		self.err_log_aug = {};  

	## CLASS UTILITY FUNCTION ================================ ## 

	def set_notification(self): 
		self.notify = 1; 

	def unset_notification(self): 
		self.notify = 0; 

	def assert_dfsa(self, descriptor, condition):
		if (self.notify):
			sys.stderr.write("DFSA Exception: "+\
				str(descriptor)+'\t'+str(condition)+'\n'); 

	def err_dfsa(self, descriptor, condition):
		if (1 or self.notify):
			sys.stderr.write("DFSA irrecoverable ERROR: " \
				+ str(descriptor) + '\t' + str(condition)+'\n');
		sys.exit(0);

	def err_dfsa_list(self, descriptor, condition, err_list):
		if (1 or self.notify):
			sys.stderr.write("DFSA irrecoverable ERROR: " \
				+ str(descriptor) + '\t' + str(condition)+'\n');
			print err_list; 
		sys.exit(0);

	def clear_err_log(self): 
		self.err_log = []; 
		self.err_log_aug = {};  

	def log_dfsa(self, descriptor, condition):
		err_line = "DFSA ERROR: " \
			+ str(descriptor) + '\t' + str(condition)+'\n';
		if (self.notify): 
			sys.stderr.write(err_line); 
		self.err_log.append(err_line); 

	def log_dfsa_list(self, descriptor, condition, err_list):
		err_line = "DFSA ERROR: " \
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
		print "\nDFSA", self.name, "ERRORS:", len(self.err_log); 
		for entry in self.err_log: 
			print entry.strip(); 
			if (entry in self.err_log_aug): 
				print '\t', self.err_log_aug[entry]; 
		print 'END LOG....\n'; 

	def transition_display(self, pair, destination): 
		newstring = "(<"; 
		newstring += pair[0]; 
		newstring += ', '; 
		newstring += pair[1]; 
		newstring += '> ==> '; 
		newstring += destination; 
		newstring += ') '; 
		return newstring; 

	def import_desc(self, description): 
		self.states = description.states; 
		self.delta = description.delta; 
		self.initial = description.initial; 
		self.finals = description.finals; 
		self.sigma = description.sigma; 
		self.curr_state = self.initial; 

	def present_delta(self): 
		return self.delta; 

	def present_finals(self): 
		return self.finals; 

	def present_states(self): 
		return self.states; 

	def present_initial(self): 
		return self.initial; 

	## DFA operations functions =========================== ## 

	def symbol_sets_rec(self, rem_len, curr_sym): 
		if (rem_len == 1): 
			return [[curr_sym, ]]; 
		all_children_sets = []; 
		for symbol in self.sigma: 
			childsets = self.symbol_sets_rec(rem_len - 1, symbol); 
			for setx in childsets: 
				nextset = setx + [curr_sym, ]; 
				all_children_sets.append(nextset); 
		return all_children_sets; 

	def symbol_sets(self, length): 
		new_set = []; 
		for symbol in self.sigma: 
			new_set += self.symbol_sets_rec(length, symbol); 
		return new_set; 

	def transition(self, symbol): 
		new_state = self.delta[(self.curr_state, symbol)]; 
		self.curr_state = new_state; 
		return new_state; 

	## DFA constitution checks at import ======================== ##

	def check_desc_states(self): 
		seen_states = []; 
		for state in self.states: 
			if (state not in seen_states): 
				seen_states.append(state); 
			else: 
				self.log_dfsa("DUPLICATE STATE:", state); 
		if (self.initial not in self.states): 
			self.log_dfsa("INITIAL NOT A STATE:", self.initial); 
		for fstate in self.finals: 
			if (fstate not in self.states): 
				self.log_dfsa("SOME FINAL NOT A STATE:", fstate); 
		for pair in self.delta: 
			if (pair[0] not in self.states): 
				self.log_dfsa("TRANSITION ORIGIN NON-EXISTANT", \
					self.transition_display()); 
			if (self.delta[pair] not in self.states): 
				self.log_dfsa("TRANSITION DESTINATION NON-EXISTANT", \
					self.transition_display()); 
		return 1; 

	def check_desc_sigma(self): 
		seen_symbols = []; 
		for symbol in self.sigma: 
			if (symbol not in seen_symbols): 
				seen_symbols.append(symbol); 
			else: 
				self.log_dfsa("DUPLICATE SYMBOL", symbol); 
		for pair in self.delta: 
			if (pair[1] not in self.sigma): 
				self.log_dfsa("TRANSITION SYMBOL NON-EXISTANT", pair[1]); 
		return 1; 

	def check_desc_delta(self): 
		seen_transitions = []; 
		for pair in self.delta: 
			if (pair not in seen_transitions): 
				seen_transitions.append(pair); 
			else: 
				self.log_dfsa("DUPLICATE TRANSITION", pair[0]+','+pair[1]); 
		for state in self.states: 
			for symbol in self.sigma: 
				if ((state, symbol) not in self.delta): 
					self.log_dfsa("TRANSITION MISSING:", \
						self.transition_display((state, symbol), "q'")); 

	def check_desc_isDFA(self): 
		self.check_desc_states(); 
 		self.check_desc_sigma(); 
		self.check_desc_delta(); 

	## DFA triviality checks at import ======================== ##

	def check_whether_sigmastar(self): 
		sigma_star = 1; 
		for state in self.reacheable.keys(): 
			if state not in self.finals: 
				sigma_star = 0; 
		if (sigma_star): 
			self.log_dfsa("TRIVIAL LANGUAGE", "sigma*"); 

	def check_states_reacheable(self, test_states): 
		self.reacheable = {}; 
		sigma_star = self.symbol_sets(self.states.__len__()); 
		for sigma_string in sigma_star: 
			self.curr_state = self.initial; 
			for symbol in sigma_string: 
				if (self.transition(symbol) not in self.reacheable): 
					self.reacheable[self.curr_state] = 1; 
				else: 
					self.reacheable[self.curr_state] += 1; 
		unreacheable = []; 
		for state in self.states: 
			if (state not in self.reacheable): 
				unreacheable.append(state); 
		return DISCRETE.setintersect(unreacheable, test_states);

	def check_finals_reacheable(self): 
		unreacheable = self.check_states_reacheable(self.finals); 
		if (unreacheable.__len__()): 
			self.log_dfsa_list("UNREACHEABLE FINAL STATES", "", \
				unreacheable); 

	def check_nonempty(self): 
		unreacheable = self.check_states_reacheable(self.states); 
		if (not DISCRETE.setminus(self.finals, unreacheable).__len__()): 
			self.log_dfsa("EMPTY LANGUAGE", ""); 

	def check_allstates_reacheable(self): 
		unreacheable = self.check_states_reacheable(self.states); 
		if (unreacheable.__len__()): 
			self.log_dfsa_list("USELESS STATES", "", unreacheable); 

	def check_desc_DFA_nontrivial(self): 
		self.check_nonempty(); 
		self.check_whether_sigmastar(); 
		self.check_finals_reacheable(); 
		self.check_allstates_reacheable(); 

## <=================================>
## END DFSA CLASS ===================;

def test_dfa(): 
	dfsa = deterministic_finite_state_automaton("test"); 
	desc1 = DFADSC.form_desc1();
	err_desc1 = DFADSC.form_err_desc1();
	err_desc2 = DFADSC.form_err_desc2(); 

	dfsa.unset_notification(); 
	dfsa.import_desc(err_desc2); 
	dfsa.check_desc_isDFA();   

	#print dfsa.symbol_sets(4); 
	dfsa.check_desc_DFA_nontrivial(); 
	dfsa.show_log(); 

def test2(): 
	desc1 = DFADSC.form_desc1();
	desc2 = DFADSC.form_desc2(); 
	err_desc1 = DFADSC.form_err_desc1();
	err_desc2 = DFADSC.form_err_desc2(); 

	dfsa_1 = deterministic_finite_state_automaton("test1"); 
	dfsa_1.unset_notification(); 
	dfsa_1.import_desc(desc1); 
	dfsa_1.check_desc_isDFA();   
	dfsa_1.check_desc_DFA_nontrivial(); 

	dfsa_2 = deterministic_finite_state_automaton("test2"); 
	dfsa_2.unset_notification(); 
	dfsa_2.import_desc(desc2); 
	dfsa_2.check_desc_isDFA();   
	dfsa_2.check_desc_DFA_nontrivial(); 

	return (dfsa_1, dfsa_2); 

#test_dfa(); 
