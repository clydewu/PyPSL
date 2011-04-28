#!/usr/bin/env python2.5

import sys

'''Quick & dirty, not very well tested Public Suffix List support for Python.

    This script expects "effective_tld_names.dat" (see below) to exist in the
    current working directory. When executed, reads the file and writes to
    standard output the source code for a Python module that exports a single
    lookup() function. Calling this function with a DNS name will return the
    public suffix for that name, e.g.

        www.foo.bar.baz.com -> baz.com
        my.hospital.nhs.uk -> hospital.nhs.uk
        some.company.co.uk -> company.co.uk

    effective_tld_names.dat can be retrieved from:

        http://publicsuffix.org/list/
'''


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

def add_rule(root, rule):
    if rule.startswith('!'):
        negate = 1
        rule = rule[1:]
    else:
        negate = 0

    parts = rule.split('.')
    find_node(root, parts)[0] = negate

def simplify(node):
    if len(node) == 1:
        return node[0]

    return (node[0], dict((k, simplify(v))
                          for (k, v) in node[1].iteritems()))

def mini_pformat(o):
    if o in (0, 1):
        return str(o)
    elif type(o) in (str, unicode):
        return repr(o)
    elif type(o) is dict:
        return '{' + ','.join((mini_pformat(k)+':'+mini_pformat(v))
                              for (k, v) in o.iteritems()) + '}'
    else:
        assert type(o) == tuple
        if len(o) == 1:
            return '(%s,)' % mini_pformat(o2[0])
        else:
            return '(' + ','.join(mini_pformat(o2) for o2 in o) + ')'


def build_structure(fp):
    root = [0]

    for line in fp:
        line = line.decode('utf-8').strip()
        if line.startswith('//') or not line:
            continue

        add_rule(root, line.split()[0])

    return root


def main():
    if len(sys.argv) != 2:
	print "Argument error: filename"
	exit()
    root = build_structure(file(sys.argv[1]))
    root = simplify(root)
    write_module(root)

def write_module(root):
    print '#!/usr/bin/env python'
    print
    print 'psl =', mini_pformat(root)
    print


if __name__ == '__main__':
    main()

