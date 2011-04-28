#!/usr/bin/env python

import sys

# every nodes could be a tuple or a integer
# schema of tuple : (excp_rule, treenode)
# Note 'treenode' is differenet from 'node' since 'treenode' may include serval 'node's.
psl = ( 0, {'com':0, 'jp': (0, {'*':0, 'hokkaido':(0, {'*':0, 'pref':1}), 'tokyo':(0, {'*': 0, 'metro': 1})})})

# return a list
# None : no match
# 0 : Match, Normal Rule
# 1 : Match, Exception Rule
def getMatchesFromLabels(labels):
    def match_label(matches, depth, tree, labels):
	if tree is not None:
	    if isinstance(tree, tuple):
		excp_rule, tree_node = tree
		if(depth != 0):
		    matches[-depth] = excp_rule
		#print "Lv " + str(depth) + " t"  + str(matches)
		#print str(matches)
		if depth < len(labels):
		    subtree = tree_node.get(labels[-(depth+1)], tree_node.get('*', None))
		else:
		    subtree = None
		if subtree is not None:
		    #print "MATCH! subtree of next is " + labels[-(depth+1)] + ":"  + str(subtree)
		    pass
		match_label(matches, depth+1, subtree, labels)
	    else:
		matches[-depth] = tree
		#print "Lv " + str(depth) + " i" + str(matches)
		#print str(matches)
	else:
	    pass
	    #raise Exception('PSL Tree is None')

    matches = [None] * (len(labels))
    match_label(matches, 0, psl, labels)
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
	    print getMatchesFromLabels(domain.split('.'))
	    print getPublicSuffix(domain)
	    print isUnderPublicSuffix(domain)
    else:

	print "isPublicSuffix(\"www.metro.tokyo.jp\")"
	print isPublicSuffix("www.metro.tokyo.jp")
	print "isPublicSuffix(\"metro.tokyo.jp\")"
	print isPublicSuffix("metro.tokyo.jp")
	print "isPublicSuffix(\"www.tokyo.jp\")"
	print isPublicSuffix("www.tokyo.jp")
	print "isPublicSuffix(\"tokyo.jp\")"
	print isPublicSuffix("tokyo.jp")

	print
	print "hasPublicSuffix(\"www.metro.tokyo.jp\")"
	print hasPublicSuffix("www.metro.tokyo.jp")
	print "hasPublicSuffix(\"metro.tokyo.jp\")"
	print hasPublicSuffix("metro.tokyo.jp")
	print "hasPublicSuffix(\"www.tokyo.jp\")"
	print hasPublicSuffix("www.tokyo.jp")
	print "hasPublicSuffix(\"tokyo.jp\")"
	print hasPublicSuffix("tokyo.jp")
	print "hasPublicSuffix(\"tokyo.xxx\")"
	print hasPublicSuffix("tokyo.xxx")

	print
	print "isUnderPublicSuffix(\"www.metro.tokyo.jp\")"
	print isUnderPublicSuffix("www.metro.tokyo.jp")
	print "isUnderPublicSuffix(\"metro.tokyo.jp\")"
	print isUnderPublicSuffix("metro.tokyo.jp")
	print "isUnderPublicSuffix(\"www.tokyo.jp\")"
	print isUnderPublicSuffix("www.tokyo.jp")
	print "isUnderPublicSuffix(\"tokyo.jp\")"
	print isUnderPublicSuffix("tokyo.jp")
