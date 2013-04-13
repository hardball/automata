#!/usr/bin/python 

import sys, re, math, os; 

## Global Regular Expressions
## =========================>
regex_xml = re.compile(r'^\<.*\>$');
regex_eliminate = re.compile(r'(\"|\')');
regex_sep = re.compile(r'.*(\.|\,|\;|\!|\?)$');
regex_separator = re.compile(r'(\.|\,|\;|\!|\?)');
regex_pause = re.compile(r'^(\.|\,|\;|\!|\?)$');
regex_separatorx = re.compile(r'(\.|\,|\;|\!|\?\'\"\&\%\$\#\@\+)');

regex_period = re.compile(r'.*\.');
regex_comma = re.compile(r'.*\,');
regex_semi = re.compile(r'.*\;');
regex_excl = re.compile(r'.*\!');
regex_question = re.compile(r'.*\?');

regex_blogs = re.compile(r'^blog.*txt$');
regex_dir_hidden = re.compile(r'^\..*');

regex_dottxt = re.compile(r'\.txt');
regex_dottagged = re.compile(r'\.tagged');
regex_slash = re.compile(r'\/');

separator_list = [regex_period, regex_comma, regex_semi, \
				regex_excl, regex_question];
separators = ['.', ',', ';', '!', '?'];

regex_tagged = re.compile(r'^tagged\..*');

regex_alphaplus = re.compile(r'^.*[A-Za-z]+.*$');
regex_notalpha = re.compile(r'[^A-Za-z]+');
regex_alphanum = re.compile(r'^[A-Za-z0-9]+$');
regex_notalphanum = re.compile(r'[^A-Za-z0-9]+');
regex_alpha_param = re.compile(r'(^\([0-9]+$|^[0-9]+\)$)');

regex_for = re.compile(r'^\*?for$');
regex_ing = re.compile(r'^[A-Za-z]*ing$');
regex_for_param = re.compile(r'^\*?for\)$');
regex_ing_param = re.compile(r'^[A-Za-z]*ing\)$');

regex_param = re.compile(r'(^\(.*$|^.*\)$)');
regex_paramu = re.compile(r'^\(.*$');
regex_paraml = re.compile(r'^.*\)$');
regex_oddassert = re.compile(r'^the odd assert.*');

regex_starpos = re.compile(r'\*');
regex_pupper = re.compile(r'\(');
regex_plower = re.compile(r'\)');
regex_capital = re.compile(r'^[A-Z].*$');

regex_VB = re.compile(r'^VB.*$');
regex_proper = re.compile(r'^[A-Z]+.*$');
regex_elim = re.compile(r'(\.|\,|\;|\!|\?|\'|\"|\&|\%|\$|\#|\@|\+)');
regex_elim2 = re.compile(r'(\.|\,|\;|\!|\?|\'|\"|\&|\%|\$|\#|\@|\+|\_)');

regex_modal_file = re.compile(r'\..*');

regex_begindiv = re.compile(r'\<div.*\>'); 
regex_enddiv = re.compile(r'\<\/div\>');
regex_beginul = re.compile(r'\<ul.*\>'); 
regex_endul = re.compile(r'\<\/ul\>'); 

sregex_lxml_format = re.compile(r'\>$'); 
sregex_ubegindiv = re.compile(r'^\<div'); 
sregex_udivid = re.compile(r'^\ ?id\=\"'); 
sregex_ldivid = re.compile(r'\"\ ?$'); 
sregex_u_ulline = re.compile(r'^\<li[A-Za-z0-9]*\>'); 
sregex_l_ulline = re.compile(r'<\/li\>$'); 

## <===============================
## End Global Regular Expressions

##================================
## BEGIN SYSTEM AND FILE FUNCTIONS

def syscall(cmd, args):
	cmdln = cmd;
	for arg in args:
		cmdln += ' ';
		cmdln += arg; 
	print cmdln;
	p = os.popen(cmdln)
	results = p.readlines()
	p.close()
	return results

def print_list(listx):
	for entry in listx:
		print entry;

def get_files_x(directory):
	cmd = 'ls';
	args = ['-al', directory];
	results = syscall(cmd, args);
	file_list = [];
	for line in results:
		words = line.strip().split();
		if (len(words) >= 8):
			if (not(regex_dir_hidden.match(words[len(words)-1]))):
				#newword = "../blogs/american_italy/";
				newword = '';
				newword += directory;
				newword += words[len(words)-1];
				print newword;
				file_list.append(newword);
	#sys.exit(0); 
	return file_list;

def get_files_xnt(directory):
	cmd = 'ls';
	args = ['-al', directory];
	results = syscall(cmd, args);
	file_list = [];
	for line in results:
		words = line.strip().split();
		if (len(words) >= 8):
			if (not(regex_dir_hidden.match(words[7]))) and \
				(not(regex_tagged.match(words[7]))):
				#newword = "../blogs/american_italy/";
				newword = '';
				newword += directory;
				newword += words[7];
				print newword;
				file_list.append(newword);
	return file_list;

def get_files():
	cmd = 'ls';
	args = ['-al', './'];
	results = syscall(cmd, args);
	file_list = [];
	for line in results:
		words = line.strip().split();
		if len(words) >= 8:
			#newword = "../blogs/american_italy/";
			newword = '';
			newword += words[7];
			print newword;
			file_list.append(newword);
	return file_list; 

def read_file(file_name): 
	handle = open(file_name, 'r'); 
	lines = handle.readlines(); 
	handle.close(); 
	newlines = []; 
	for line in lines: 
		newlines.append(line.strip()); 
	return newlines; 

def process_file(file_name):
	print file_name;
	handle = open(file_name, 'r');
	lines = handle.readlines();
	handle.close();
	return process_text(lines);

def process_text(newtext):
	all_words = []
	for line in newtext:
		words = line.strip().split();
		for word in words:
			all_words.append(word);
	new_words = []
	for word in all_words:
		xlist = separator_cast(word);
		for elem in xlist:
			new_words.append(elem.lower());
	return new_words;

def separator_cast(word):
	xlist = []
	if regex_sep.match(word):
		xlist.append(regex_separator.sub('', word));
		for i in range(0, len(separators), 1):
			if (separator_list[i]).match(word):
				xlist.append(separators[i]);
	else:
		xlist.append(word);
	return xlist;

def process_files(file_names):
	word_list = []
	tmp_list = []
	for name in file_names:
		curr_list = process_file(name);
		tmp_list += curr_list;
	for tmp in tmp_list:
		if ((tmp != '') and not (regex_xml.match(tmp))):
			tmp = regex_eliminate.sub('', tmp);
			if (not (regex_separator.match(tmp))):
				tmp = regex_separatorx.sub(' ', tmp);
			word_list.append(tmp.lower());
	del tmp_list;
	return word_list;

def process_one_text(text):
	"""takes one part of the output form get_line_sets"""
	word_set = {}
	word_list = [];
	for line in text:
		words = line.strip().split();
		for word in words:
			word_list.append(word);
	for tmp in word_list:
		if ((tmp != '') and not (regex_xml.match(tmp))):
			tmp = regex_eliminate.sub('', tmp);
			if (not (regex_separator.match(tmp))):
				tmp = regex_separatorx.sub(' ', tmp);
			tmp = tmp.lower();
			if tmp not in word_set:
				word_set[tmp] = 1;
			else:
				word_set[tmp] += 1;
	return word_set;

def process_one_tagged_text(text):
	"""takes one part of the output form get_line_sets"""
	word_set = {}
	word_list = [];
	for word in text:
		word_list.append(word[0]);
	for tmp in word_list:
		if ((tmp != '') and not (regex_xml.match(tmp))):
			tmp = regex_eliminate.sub('', tmp);
			if (not (regex_separator.match(tmp))):
				tmp = regex_separatorx.sub(' ', tmp);
			tmp = tmp.lower();
			if tmp not in word_set:
				word_set[tmp] = 1;
			else:
				word_set[tmp] += 1;
	return word_set;

## END SYSTEM AND FILE FUNCTIONS
##==============================

##=========================================
## BEGIN XML DFA DESCRIPTION FILE FUNCTIONS

def strip_xml_line(linein): 
	lineout = ""; 
	fstate = 0; 
	for lit in linein: 
		if ((lit == '<') and (fstate == 0)): 
			fstate = 1; 
		elif ((lit == '>') and (fstate == 1)): 
			fstate = 2; 
		elif ((lit not in ['<', '>', '/']) and (fstate == 2)): 
			fstate = 0; 
		if (not fstate): 
			lineout += lit; 
		#print linein, fstate, lit; 
	return lineout; 

def parse_divid(begindiv_line): 
	imm_stringx = sregex_ubegindiv.sub("", begindiv_line); 
	divstripped = sregex_lxml_format.sub("", imm_stringx); 
	imm_stringy = sregex_udivid.sub("", divstripped); 
	divid = sregex_ldivid.sub("", imm_stringy); 
	return divid; 

def parse_divs(linesin): 
	divs = {};  
	dstate = 0; 
	curr_div = []; 
	for line in linesin: 
		if (regex_begindiv.match(line)): 
			dstate += 1;
			divid = parse_divid(line); 
		elif (regex_enddiv.match(line)): 
			dstate -= 1; 
			divs[divid] = curr_div; 
			curr_div = []; 

		#print curr_div, line, dstate; 
		if ((dstate == 1) and (not regex_begindiv.match(line))): 
			curr_div.append(line); 
	return divs;

def parse_divs_raw(linesin): 
	divs = {};  
	dstate = 0; 
	curr_div = []; 
	for line in linesin: 
		if (regex_begindiv.match(line)): 
			dstate += 1;
			divid = parse_divid(line); 
		elif (regex_enddiv.match(line)): 
			dstate -= 1; 
			divs[divid] = curr_div; 
			curr_div = []; 

		#print curr_div, line, dstate; 
		curr_div.append(line); 
	return divs;

def seek_name(divsin): 
	name = ""; 
	hasname = 0; 
	for div in divsin: 
		#print div, divsin[div]; 
		if (div.strip() != "NAME"): 
			continue; 
		for line in divsin[div]: 
			#print line, type(line); 
			if (line.strip().__len__()): 
				name = line; 
	return name; 

def parse_uls(linesin): 
	ul = [];
	ul_lines = [];  
	ustate = 0; 
	for line in linesin: 
		if (regex_beginul.match(line)): 
			ustate += 1; 
		if (regex_endul.match(line)): 
			ustate -= 1; 

		if ((ustate == 1) and (not regex_beginul.match(line))): 
			ul_lines.append(line); 
	#print ul_lines; 
	for line in ul_lines: 
		imm_string = sregex_u_ulline.sub("", line); 
		ulstripped = sregex_l_ulline.sub("", imm_string); 
		if (line.strip().__len__()): 
			ul.append(ulstripped); 
	#print ul; 
	return ul; 

## END XML DFA DESCRIPTION FILE FUNCTIONS
##=======================================

