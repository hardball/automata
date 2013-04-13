#!/usr/bin/python
import math;

##BEGIN DISCRETE PROBABILITY
##=========================>

def histogram(listx):
	histogram = {};
	for elem in listx:
		if (elem not in histogram):
			histogram[elem] = 1;
		else:
			histogram[elem] += 1;
	return histogram;

def freq_distribution(dictx):
	frequencies = {};
	for elem in dictx:
		cnt = dictx[elem];
		if (cnt not in frequencies):
			frequencies[cnt] = 1;
		else:
			frequencies[cnt] += 1;
	return frequencies;

## <=======================
## END DISCRETE PROBABILITY

##BEGIN SET THEORETIC FUNCTIONS
##============================>

def setunion(setx, sety):
	setxy = [];
	for x in setx:
		setxy.append(x);
	for y in sety:
		if (y not in setx):
			setxy.append(y);
	return setxy;

def setintersect(setx, sety):
	setxy = [];
	for x in setx:
		if (x in sety):
			setxy.append(x);
	return setxy;

def setminus(setx, sety):
	setxy = [];
	for x in setx:
		if (x not in sety):
			setxy.append(x);
	return setxy;

def setsymdiff(setx, sety):
	setxy = [];
	for x in setx:
		if (x not in sety):
			setxy.append(x);
	for y in sety:
		if (y not in setx):
			setxy.append(y);
	return setxy;

def is_subset(setx, sety):
	for x in setx:
		if (x not in sety):
			return 0;
	return 1;

def is_nsubset(setx, sety, n):
	cnt = 0;
	tested = {};
	for x in setx:
		if (x not in sety):
			if (x not in tested):
				cnt += 1;
				tested[x] = 1;
			else:
				tested[x] += 1;
	if (cnt <= n):
		return 1;
	else:
		return 0;

def is_superset(setx, sety):
	for y in sety:
		if (y not in setx):
			return 0;
	return 1;

def is_nsuperset(setx, sety, n):
	cnt = 0;
	for y in sety:
		if (y not in setx):
			if (y not in tested):
				cnt += 1;
				tested[y] = 1;
			else:
				tested[y] += 1;
	if (cnt <= n):
		return 1;
	else:
		return 0;

def subsets_rec(set0, d):
	if (d > 1):
		#print set0, d;
		newset = [];
		for elem in set0:
			set1 = set0[:]
			set1.remove(elem);
			subsets1 = subsets_rec(set1, d-1);
			for ss in subsets1:
				newset.append(ss + [elem,]);
		return newset;
	elif (d <= 0):
		return [[]];
	else:
		newset = [];
		for elem in set0:
			newset.append([elem,]);
		return newset;

def subsets_n(set0, n):
	if (n > len(set0)):
		print "yrequired subset size too large";
		return [set0,];
	subsets = subsets_rec(set0, n);
	#print subsets, n, len(subsets);
	return subsets;

def subsets(set0, size):
	if (size > len(set0)):
		print set0, len(set0), size;
		print "xrequired subset size too large";
		size = len(set0);
	set0x = [];
	for elem in set0:
		if (elem not in set0x):
			set0x.append(elem);
	set0x.sort();
	all_subsets = [];
	if (size <= -1):
		for i in range(0, len(set0)+1, 1):
			all_subsets += subsets_n(set0x, i);
	else:
		all_subsets = subsets_n(set0x, size);
	new_subsets = [];
	#print set0, len(all_subsets);
	#for subset in all_subsets:
	#	if (subset not in new_subsets):
	#		new_subsets.append(subset);
	#		sys.stderr.write('>');
	#	else:
	#		print "SUBSETS DUPLICATION!!";
	return all_subsets;

def uor_subsets_rec(set0, d):
	print ' '*(3-d), set0, d;
	if ((d > 0) and (len(set0) >= 1)):
		set1 = set0[1:len(set0)];
		newset0 = [];
		newset0 += uor_subsets_nrec(set0, d-1);
		newset1 = [];
		for ss in newset0:
			newset1.append(ss + [set0[0],]);
		#print ' '*(3-d), newset1;
		newset1 += uor_subsets_nrec(set1, d);
		#print ' '*(3-d), newset1;
		return newset1;
	elif ((d > 0) and (len(set0) < 1)):
		return [];
	else: ## d <= 0;
		return [[]];

def uo_subsets_nrec(set0, d):
	#print ' '*(3-d), set0, d;
	if ((d > 0) and (len(set0) >= 1)):
		set1 = set0[1:len(set0)];
		newset0 = uo_subsets_nrec(set1, d);
		newset1 = uo_subsets_nrec(set1, d-1);
		for ss in newset1:
			newset0.append(ss + [set0[0]]);
		return newset0;
	elif ((d > 0) and (len(set0) < 1)):
		return [];
	else: ## d <= 0;
		return [[]];

def uo_subsets_n(set0, n):
	if (n > len(set0)):
		print "required subset size too large";
		return [set0,];
	subsets = uo_subsets_nrec(set0, n);
	#print "original:", set0, n;
	return subsets;

def uo_subsets(set0, size):
	if (size > len(set0)):
		print "required subset size too large";
		size = len(set0);
	set0x = [];
	for elem in set0:
		if (elem not in set0x):
			set0x.append(elem);
	#print set0x;
	set0x.sort();
	if (size < 0):
		new_subsets = [];
		for n in range(0, len(set0)+1, 1):
			n_subsets = uo_subsets_n(set0x, n);
			#print n, n_subsets;
			new_subsets += n_subsets;
	else:
		new_subsets = uo_subsets_n(set0x, size);
	return new_subsets;


def AND(nlist):
	for x in nlist:
		if (not x):
			return 0;
	return 1;

def OR(nlist):
	for x in nlist:
		if (x):
			return 1;
	return 0;

def XOR(nlist):
	w = nlist[0];
	if (len(nlist) < 2):
		return w;
	for i in range(1, len(nlist), 1):
		x = nlist[i];
		if (x or w) and (not (x and w)):
			w = 1;
		else:
			w = 0;
	return w;

## <==========================
## END SET THEORETIC FUNCTIONS

## BEGIN PERMUTATIONS AND POSETS
## ============================>

class permutation:

	def __init__(self):
		self.initial_set = [];
		self.permutations = [];

	def initialize(self, new_set):
		self.initial_set = new_set;
		self.permutations = [];

	def set_permutations_rec(self, partial, remainder):
		if (len(remainder) == 0):
			self.permutations.append(partial);
			return;
		for i in range(0, len(remainder), 1):
			new_remainder = remainder[0:i] + remainder[i+1:len(remainder)];
			new_partial = partial + [remainder[i], ];
			self.set_permutations_rec(new_partial, new_remainder);
		return;

	def set_permutations(self):
		permutations = [];
		self.set_permutations_rec([], self.initial_set);

	def present_permutations(self):
		return self.permutations;

## <==========================
## END PERMUTATIONS AND POSETS

cperm = permutation();

def testx():
	permx = permutation();
	permx.initialize(['a', 'b', 'c', 'd']);
	permx.set_permutations();
	print permx.present_permutations();

#testx();

