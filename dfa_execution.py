#!/usr/bin/python 

import sys, re; 
import math as M; 
import random as R; 
import string as S; 

## BEGIN DFAEXEC CLASS ==================
## =====================================>

class dfa_execution: 

	def __init__(self): 
		self.initial_state = ""; 
		self.curr_state = ""; 
		self.terminal_state = ""; 
		
		self.curr_string = "";
		self.curr_start = 'x'; 

		self.test = {};  
		self.acceptance = []; 
		self.weights = []; 

		self.seq_accept = []; 

	def import_components(self, delta, finals, initial): 
		self.this_delta = delta; 
		self.this_finals = finals; 
		self.initial_state = initial; 

	def import_test(self, test): 
		self.test = test; 

	def present_termination(self): 
		return self.terminal_state; 

	def set_conditions(self, new_initial, string): 
		self.curr_state = new_initial; 
		self.curr_listring = []; 
		for lit in string: 
			self.curr_listring.append(lit);
		self.curr_listring.reverse();  

	def execute(self): 
		while (len(self.curr_listring)): 
			self.curr_state = \
				self.this_delta[\
					(self.curr_state, self.curr_listring.pop())]; 
		self.terminal_state = self.curr_state; 
		return (self.terminal_state in self.this_finals); 

	def execute_test(self): 
		self.acceptance = []; 
		self.weights = []; 
		for entry in self.test: 
			test_string = self.test[entry][0]; 
			potential_score = int(self.test[entry][1]); 
			if (self.test[entry][2] == 'x'): 
				self.set_conditions(self.initial_state, test_string); 
			else: 
				self.set_conditions(self.test[entry][2], test_string); 
			accept = self.execute(); 
			self.acceptance.append(accept); 
			self.weights.append(potential_score); 
		return self.acceptance; 

	def present_curr_weights(self): 
		return self.weights; 

	def execute_continuous(self): 
		self.seq_accept = []; 
		while (len(self.curr_listring)): 
			self.curr_state = \
				self.this_delta[\
					(self.curr_state, self.curr_listring.pop())]; 
			self.seq_accept.append(self.curr_state in self.this_finals); 
		return self.seq_accept; 

	def execute_test_continuous(self): 
		self.acceptance = []; 
		self.weights = []; 
		for entry in self.test: 
			test_string = self.test[entry][0]; 
			potential_score = int(self.test[entry][1]); 
			if (self.test[entry][2] == 'x'): 
				self.set_conditions(self.initial_state, test_string); 
			else: 
				self.set_conditions(self.test[entry][2], test_string); 
			seq_accept = self.execute_continuous(); 
			self.acceptance.append(seq_accept); 
			self.weights.append(potential_score); 
		return self.acceptance; 

## <====================================>
## END DFAEXEC CLASS ===================;

