#!/usr/bin/python

import sys, re; 
import math as M; 
import random as R; 
import string as S; 

import data_io as DIO; 

## BEGIN DFA DESC CLASS ==================
## ======================================>

class DFA_descript: 
	## struct-like description that can be used by the rest of the system;

	def __init__(self, name): 
		self.name = name; 
		
		self.states = []; 
		## list of name_strings for each state; 		

		self.delta = {}; 
		## a dictionary that forms the dalta function of the DFA; 
		## each entry has a key that is a pair (q, a); 
		##		where q := current state, a := current symbol; 
		## each entry has a singleton value q' := next state; 

		self.initial = ""; 
		## single string defining the initial state; 

		self.finals = []; 
		## list of strings defining the accepting states; 

		self.sigma = []; 
		## legal alphabets used for symbols in this machine; 

	def add_state(self, new_state): 
		self.states.append(new_state); 

	def add_transition(self, source, symbol, destination): 
		self.delta[(source, symbol)] = destination; 

	def define_initial(self, initial): 
		self.initial = initial; 

	def add_final(self, new_final): 
		self.finals.append(new_final); 

	def add_symbol(self, new_symbol): 
		self.sigma.append(new_symbol); 

	def present_symbols(self): 
		return self.sigma; 

	def present_states(self): 
		return self.states; 

	def display_transition(self, pair, destination): 
		newstring = "\t(<"; 
		newstring += pair[0]; 
		newstring += ', '; 
		newstring += pair[1]; 
		newstring += '> ==> '; 
		newstring += destination; 
		newstring += ') '; 
		print newstring;  

	def show_description(self): 
		print "NAME:", self.name; 
		print "STATES:", self.states; 
		print "DELTA:"; 
		for pair in self.delta: 
			self.display_transition(pair, self.delta[pair]); 
		print "FINALS:", self.finals; 
		print "SIGMA:", self.sigma; 

## ====================================>
## END DFA DESC CLASS ==================

## BEGIN DFA DESC READER CLASS ==================
## =============================================>

class DFA_descript_read: 
	## allows frequently used descriptions (solution DFAs) 
	## to be read in from a file format; 

	def __init__(self): 
		self.notify = 0; 

		self.description_dir = "./"; 
		self.description_files = []; 
		self.description_structs = {}; 
		
		self.curr_description_name = ""; 
		self.curr_description_struct = {}; 

		self.dscriptions = {}; 

	def set_notification(self): 
		self.notify = 1; 

	def unset_notification(self): 
		self.notify = 0; 

	def assert_dfar(self, descriptor, condition):
		sys.stderr.write("DFA READING Exception: "+\
			str(descriptor)+'\t'+str(condition)+'\n'); 

	def err_dfar(self, descriptor, condition):
		sys.stderr.write("DFA READING irrecoverable ERROR: " \
			+ str(descriptor) + '\t' + str(condition)+'\n');
		sys.exit(0);

	def set_dir(self, new_dir): 
		self.description_dir = new_dir; 
		self.description_files = \
			DIO.get_files_x(self.description_dir); 
		if (self.notify): 
			print "DESCRIPTION FILES:"; 
			for dfile in self.description_files: 
				print '\t', dfile; 

	def parse_xml(self, this_file): 
		success = 1; 
		lines = DIO.read_file(this_file); 
		components_cnt = 0; 
		for line in lines: 
			newline = DIO.strip_xml_line(line); 
		divs = DIO.parse_divs(lines); 
		new_divs = {}; 
		for div in divs: 
			if (div.strip() == "NAME"): 
				continue; 
			if (div.strip() == "DELTA"): 
				delta_lines = DIO.parse_uls(divs[div]); 
				new_divs[div] = delta_lines; 
			else: 
				new_divs[div] = divs[div]; 
			components_cnt += 1; 
		if (components_cnt != 5): 
			self.assert_dfar("REQUIRED ELEMENTS LENGTH INCORRECT", \
				components_cnt); 
			return 0; 
		self.curr_description_name = DIO.seek_name(divs); 
		if (self.notify): 
			print "NAME:", self.curr_description_name; 
		self.curr_description_struct = new_divs; 
		return success; 

	def parse_xmls(self): 
		self.description_structs = {}; 
		for dfile in self.description_files: 
			if (self.parse_xml(dfile)): 
				self.description_structs[self.curr_description_name] = \
					self.curr_description_struct; 
				if (self.notify): 
					print self.curr_description_struct; 

	def treat_component(self, component_name, component_struct): 
		if (component_name == "DELTA"):
			delta_dict = {}; 
			if (self.notify): 
				print "DELTA", component_struct; 
			for line in component_struct: 
				words = line.strip().split();  
				if (len(words) != 3): 
					self.assert_dfar( \
					"Delta function entry format incorrect", len(words)); 
				else: 
					delta_dict[(words[0], words[1])] = words[2]; 
			return delta_dict; 
						
		elif (component_name == "INITIAL"): 
			if (len(component_struct) != 1): 
				self.assert_dfar( \
				"Initial state format incorrect", len(words)); 
			else: 
				words = component_struct[0].strip().split(); 
				if (len(words) != 1): 
					self.assert_dfar( \
						"Initial state format incorrect", len(words)); 
				else: 
					return words[0]; 
		else: 
			elements = []; 
			for line in component_struct: 
				words = line.strip().split(); 
				for word in words: 
					elements.append(word); 
			return elements; 

	def translate(self): 
		self.descriptions = {}; 
		for description_name in self.description_structs: 
			new_description = DFA_descript(description_name); 
			#print "DESCRPT NAME:", description_name; 
			for component_name in \
			self.description_structs[description_name]: 
				component = self.treat_component(component_name, \
					self.description_structs[description_name]\
					[component_name]); 
				if (component_name.strip() == "DELTA"): 
					for pair in component: 
						new_description.add_transition(\
							pair[0], pair[1], component[pair]); 
				elif (component_name.strip() == "INITIAL"): 
					new_description.define_initial(component); 
				elif (component_name.strip() == "STATES"): 
					for state in component: 
						new_description.add_state(state); 
				elif (component_name.strip() == "FINALS"): 
					for fstate in component: 
						new_description.add_final(fstate); 
				elif (component_name.strip() == "SIGMA"): 
					for sigma in component: 
						new_description.add_symbol(sigma); 
			self.descriptions[description_name] = new_description; 
			self.descriptions[description_name].show_description(); 

	def present_dfa_names(self): 
		#print "DSEC KEYS:", self.descriptions.keys(); 
		return self.descriptions.keys(); 

	def present_dfa_descript(self, name): 
		if (name not in self.descriptions): 
			self.err_dfar("DFA DEFINITION NOT IN DATABASE:", name); 
		else: 
			return self.descriptions[name]; 

## ===========================================>
## END DFA DESC READER CLASS ==================

def test_xml(): 
	test_file = "./sol_DFAs/test_dfa1.html"; 
	lines = DIO.read_file(test_file); 
	cnt = 0; 
	for line in lines: 
		newline = DIO.strip_xml_line(line); 
		#print newline, cnt; 
		cnt += 1; 
	divs = DIO.parse_divs(lines); 
	for div in divs: 
		print div, divs[div]; 
		if (div.strip() == "DELTA"): 
			delta_lines = DIO.parse_uls(divs[div]); 
			print delta_lines;
	name = DIO.seek_name(divs); 
	print "NAME:", name; 

def test_read(): 
	dfar = DFA_descript_read(); 
	dfar.unset_notification(); 
	dfar.set_dir("./sol_DFAs/"); 
	dfar.parse_xmls(); 
	dfar.translate(); 

#test_xml(); 
#test_read(); 

## ENCODING DESCRIPTION EXAMPLES =======================> 

def form_desc1(): 
	new_desc = DFA_descript("test1");
	new_desc.add_state('q0');  
	new_desc.add_state('q1'); 
	new_desc.add_state('q2'); 
	new_desc.add_state('q3'); 

	new_desc.define_initial('q0');
	new_desc.add_final('q2'); 

	new_desc.add_transition('q0', '0', 'q1'); 
	new_desc.add_transition('q0', '1', 'q0'); 
	new_desc.add_transition('q1', '0', 'q1'); 
	new_desc.add_transition('q1', '1', 'q3'); 
	new_desc.add_transition('q2', '0', 'q3'); 
	new_desc.add_transition('q2', '1', 'q2'); 
	new_desc.add_transition('q3', '0', 'q2'); 
	new_desc.add_transition('q3', '1', 'q1'); 
 
	new_desc.add_symbol('0'); 
	new_desc.add_symbol('1'); 
	return new_desc; 

def form_desc2(): 
	new_desc = DFA_descript("test2");
	new_desc.add_state('qx');  
	new_desc.add_state('qy'); 
	new_desc.add_state('qz'); 
	new_desc.add_state('qu'); 
	new_desc.add_state('qv'); 

	new_desc.define_initial('qx');
	new_desc.add_final('qu'); 

	new_desc.add_transition('qx', '0', 'qx'); 
	new_desc.add_transition('qx', '1', 'qy'); 
	new_desc.add_transition('qy', '0', 'qz'); 
	new_desc.add_transition('qy', '1', 'qx'); 
	new_desc.add_transition('qz', '0', 'qz'); 
	new_desc.add_transition('qz', '1', 'qu'); 
	new_desc.add_transition('qu', '0', 'qv'); 
	new_desc.add_transition('qu', '1', 'qy'); 
	new_desc.add_transition('qv', '0', 'qx'); 
	new_desc.add_transition('qv', '1', 'qu'); 
 
	new_desc.add_symbol('0'); 
	new_desc.add_symbol('1'); 
	return new_desc; 

def form_err_desc1(): 
	new_desc = DFA_descript("etest1");
	new_desc.add_state('q0');  
	new_desc.add_state('q1'); 
	new_desc.add_state('q2'); 
	new_desc.add_state('q3'); 
	new_desc.add_state('q4');
	new_desc.add_state('q5');

	new_desc.define_initial('q0');
	new_desc.add_final('q2'); 
	new_desc.add_final('q4');

	new_desc.add_transition('q0', '0', 'q1'); 
	new_desc.add_transition('q0', '1', 'q0'); 
	new_desc.add_transition('q1', '0', 'q1'); 
	new_desc.add_transition('q1', '1', 'q3'); 
	new_desc.add_transition('q2', '0', 'q3'); 
	new_desc.add_transition('q2', '1', 'q2'); 
	new_desc.add_transition('q3', '0', 'q2'); 
	new_desc.add_transition('q3', '1', 'q1'); 
 
	new_desc.add_transition('q4', '0', 'q3'); 
	new_desc.add_transition('q4', '1', 'q2'); 
	new_desc.add_transition('q5', '0', 'q2'); 
	new_desc.add_transition('q5', '1', 'q1'); 
	
	new_desc.add_symbol('0'); 
	new_desc.add_symbol('1'); 
	return new_desc; 

def form_err_desc2(): 
	new_desc = DFA_descript("etest2");
	new_desc.add_state('q0');  
	new_desc.add_state('q1'); 
	new_desc.add_state('q2'); 
	new_desc.add_state('q3'); 
	new_desc.add_state('q4');
	new_desc.add_state('q5');

	new_desc.define_initial('q0');
	#new_desc.add_final('q0'); 
	#new_desc.add_final('q1'); 
	#new_desc.add_final('q2'); 
	#new_desc.add_final('q3');
	new_desc.add_final('q5'); 

	new_desc.add_transition('q0', '0', 'q1'); 
	new_desc.add_transition('q0', '1', 'q0'); 
	new_desc.add_transition('q1', '0', 'q1'); 
	new_desc.add_transition('q1', '1', 'q3'); 
	new_desc.add_transition('q2', '0', 'q3'); 
	new_desc.add_transition('q2', '1', 'q2'); 
	new_desc.add_transition('q3', '0', 'q2'); 
	new_desc.add_transition('q3', '1', 'q1'); 
 
	new_desc.add_transition('q4', '0', 'q3'); 
	new_desc.add_transition('q4', '1', 'q2'); 
	new_desc.add_transition('q5', '0', 'q2'); 
	new_desc.add_transition('q5', '1', 'q1'); 
	
	new_desc.add_symbol('0'); 
	new_desc.add_symbol('1'); 
	return new_desc; 

