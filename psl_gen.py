#!/usr/bin/env python2.5

import sys
import json

def buildStruct(fp):
    def add_rule(root, rule):
	if rule.startswith('!'):
	    negate = 1
	    rule = rule[1:]
	else:
	    negate = 0

	parts = rule.split('.')
	find_node(root, parts)[0] = negate

    def find_node(parent, parts):
	if not parts:
	    return parent

	if len(parent) == 1:
	    parent.append({})

	assert len(parent) == 2
	negate, children = parent

	child = parts.pop()
	try:
	    child = child.encode('ascii')
	except:
	    pass

	child_node = children.get(child, None)

	if not child_node:
	    children[child] = child_node = [0]

	return find_node(child_node, parts)

    # main problem
    root = [0]
    for line in fp:
        line = line.decode('utf-8').strip()
        if line.startswith('//') or not line:
            continue
	line = line.split()[0]

        add_rule(root, line)

    return root

# transform leafs from list to integer
def simplify(node):
    if len(node) == 1:
        return node[0]

    return [node[0], dict((k, simplify(v))
                          for (k, v) in node[1].iteritems())]

#Customized toString() without spaces
def getMiniString(o):
    if o in (0, 1):
        return str(o)
    elif type(o) in (str, unicode):
        return repr(o)
    elif type(o) is dict:
        return '{' + ','.join((getMiniString(k)+':'+getMiniString(v))
                              for (k, v) in o.iteritems()) + '}'
    else:
        #assert type(o) == tuple
        if len(o) == 1:
            return '(%s,)' % getMiniString(o2[0])
        else:
            return '[' + ','.join(getMiniString(o2) for o2 in o) + ']'

def getStructByRuleFile(ruleFileName):
    ruleFile = open(ruleFileName, 'r')
    struct = simplify(buildStruct(ruleFile))
    ruleFile.close()
    return struct

def saveStructAsFile(struct, pyFileName):
    pyFile = open(pyFileName, 'w')
    content = "".join(['#!/usr/bin/env python\n', 'psl=', getMiniString(struct)])
    pyFile.write(content)
    pyFile.close()

def getJsonByStruct(struct):
    return json.dumps(struct)

def main():
    if len(sys.argv) != 2:
	print "Argument error: filename"
	exit()

    struct = buildStruct(file(sys.argv[1]))
    print "struct:   " + str(struct)
    ss = simplify(struct)
    print "simplify: " + str(ss)
    saveStructAsFile(ss, 'test.txt')
    js = getJsonByStruct(ss)
    print "js:       " + str(js)
    res = json.loads(js)
    print "restruct: " + str(res)


if __name__ == '__main__':
    main()

