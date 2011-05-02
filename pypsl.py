#!/usr/bin/env python

import sys

#import psl list from psl.py
from psl import *

# every nodes could be a tuple or a integer
# schema of tuple : (excp_rule, treenode)
# Note 'treenode' is differenet from 'node' since 'treenode' may include serval 'node's.
#psl = ( 0, {'com':0, 'jp': (0, {'*':0, 'hokkaido':(0, {'*':0, 'pref':1}), 'tokyo':(0, {'*': 0, 'metro': 1})})})

# return a list
# None : no match
# 0 : Match, Normal Rule
# 1 : Match, Exception Rule

def getMatchesFromLabels(labels):
    def matchSubtree(matches, depth, tree, labels):
	if tree is not None:
	    if isinstance(tree, tuple):
		excp_rule, tree_node = tree
		if(depth != 0):
		    matches[-depth] = excp_rule
		if depth < len(labels):
		    subtree = tree_node.get(unicode(labels[-(depth+1)],'utf-8'), tree_node.get('*', None))
		else:
		    subtree = None
		matchSubtree(matches, depth+1, subtree, labels)
	    else:
		matches[-depth] = tree
	else:
	    pass

    matches = [None] * (len(labels))
    matchSubtree(matches, 0, psl, labels)
    return matches


def getPublicSuffix(domain):
    labels = domain.split('.')
    matches = getMatchesFromLabels(labels)

    for i, what in enumerate(matches):
        if what is 0:
            return '.'.join(labels[i:])

def isPublicSuffix(domain):
    labels = domain.split('.')
    matches = getMatchesFromLabels(labels)
    for m in matches:
	if m != 0:
	    return False
    return True

def hasPublicSuffix(domain):
    labels = domain.split('.')
    matches = getMatchesFromLabels(labels)
    for m in matches:
	if m is 0:
	    return True
    return False


def isUnderPublicSuffix(domain):
    labels = domain.split('.')
    matches = getMatchesFromLabels(labels)
    at_least_one_zero = False
    at_least_one_nonzero = False
    for m in matches:
	if m is 0:
	    at_least_one_zero = True
	else:
	    at_least_one_nonzero = True
    return at_least_one_zero & at_least_one_nonzero
	    

if __name__ == '__main__':
    if len(sys.argv) > 1:
	domain = sys.argv[1]
	if domain is not None:
	    print "Matches: " + str(getMatchesFromLabels(domain.split('.')))
	    print "getPublicSuffix: " + str(getPublicSuffix(domain))
	    print "isPublicSuffix: " + str(isPublicSuffix(domain))
	    print "hasPublicSuffix: " + str(hasPublicSuffix(domain))
	    print "isUnderPublicSuffix: " + str(isUnderPublicSuffix(domain))
    else:
	print "isPublicSuffix(\"www.metro.tokyo.jp\")" + str(isPublicSuffix("www.metro.tokyo.jp"))
	print "isPublicSuffix(\"metro.tokyo.jp\")" + str(isPublicSuffix("metro.tokyo.jp"))
	print "isPublicSuffix(\"www.tokyo.jp\")" + str(isPublicSuffix("www.tokyo.jp"))
	print "isPublicSuffix(\"tokyo.jp\")" + str(isPublicSuffix("tokyo.jp"))

	print
	print "hasPublicSuffix(\"www.metro.tokyo.jp\")" + str(hasPublicSuffix("www.metro.tokyo.jp"))
	print "hasPublicSuffix(\"metro.tokyo.jp\")" + str(hasPublicSuffix("metro.tokyo.jp"))
	print "hasPublicSuffix(\"www.tokyo.jp\")" + str(hasPublicSuffix("www.tokyo.jp"))
	print "hasPublicSuffix(\"tokyo.jp\")" + str(hasPublicSuffix("tokyo.jp"))
	print "hasPublicSuffix(\"tokyo.xxx\")" + str(hasPublicSuffix("tokyo.xxx"))

	print
	print "isUnderPublicSuffix(\"www.metro.tokyo.jp\")" + str(isUnderPublicSuffix("www.metro.tokyo.jp"))
	print "isUnderPublicSuffix(\"metro.tokyo.jp\")" + str(isUnderPublicSuffix("metro.tokyo.jp"))
	print "isUnderPublicSuffix(\"www.tokyo.jp\")" + str(isUnderPublicSuffix("www.tokyo.jp"))
	print "isUnderPublicSuffix(\"tokyo.jp\")" + str(isUnderPublicSuffix("tokyo.jp"))
