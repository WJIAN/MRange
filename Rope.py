# -*- coding: utf-8 -*-
'''
All the logic functions are defined here.
'''

import re

# Tie from string to array
def do_expr(p):
    if len(p) == 2:
        return p[1]
    elif len(p) == 3:
        return set([i + j for i in p[1] for j in p[2]])
    else:
        if p[2] == ',':
            return p[1] | p[3]
        elif p[2] == ',-':
            return p[1] - p[3]
        elif p[2] == ',&':
            return p[1] & p[3]
    return set()

def do_multi(p):
    if len(p) == 4:
        return p[2]
    elif len(p) == 3:
        return set([i + j for i in p[1] for j in p[2]])
    else:
        return p[1]

def do_range(p):
    if len(p) == 4:
        return parse_range(p[1], p[3])
    elif len(p) == 7:
        return get_nodes_from_db(p[1].pop(), p[3].pop(), p[5].pop())

def do_operator(p):
    return p[1];

def do_term(p):
    return set([p[1]])

def get_nodes_from_db(type, tag, status):
    #TODO mongo
    return set([type + tag + status])

def parse_range(a, b):
    re_num = re.compile("(\d+)")
    re_word = re.compile("[A-Za-z\-\._]+")
    p1 = filter(lambda x:x!='', re_num.split(a.pop()))
    p2 = filter(lambda x:x!='', re_num.split(b.pop()))

    range_list = ['']
    prefix = ''
    postfix = ''

    if re_num.match(p1[0]) and re_word.match(p2[0]) :
        prefix = p1.pop(0)

    if re_num.match(p1[-1]) and re_word.match(p2[-1]) :
        prefix = p1.pop(0)
        postfix = p2.pop(-1)

    if len(p1) != len(p2):
        #TODO throw except
        return set()

    for (i,j) in zip(p1,p2):
        if re_num.match(i) and re_num.match(j):
            append = untied_num([i, j])
        elif i == j:
            append = [i]
        else:
           #TODO throw except
           return set()

        range_list = [x + y for x in range_list for y in append]

    if prefix != '':
        range_list = [prefix + x  for x in range_list]

    if postfix != '':
        range_list = [x + postfix for x in range_list]

    return set(range_list)

def untied_num(pair):
    rezn = re.compile("^0\d+")
    ret = []
    if rezn.match(pair[0]) or rezn.match(pair[1]):
        l = len(pair[0])
        #if l != len(pair[1]): raise ErrorNodeBox, "syntax error: " + nums
        pair.sort()
        for i in range(int(pair[0]), int(pair[1]) + 1):
            si = str(i)
            ret.append('0' * (l - len(si)) + si)
    else:
        pair[0] = int(pair[0])
        pair[1] = int(pair[1])
        pair.sort()
        for i in range(pair[0], pair[1] + 1):
            ret.append(str(i))
    return ret

# --------------------------------------------------------------------------

# Untie from array to string
def build_tree(bag):
    tree = {}
    for i in bag:
        root = tree
        for token in re.findall("(\d+|\D+)", i):
            if token not in root.keys(): root[token] = {}
            root = root[token]
        root[''] = ''
    return tree

def travel_tree(tree):
    return do_trav(tree)[0]

def do_trav(tree):
    postfix = {}

    for k, v in tree.items():
        if k == '' and len(tree) == 1: return '', 0
        flag = 0
        if isinstance(v, dict): v, flag = do_trav(v)
        if flag:
            if '' not in postfix.keys(): postfix[''] = []
            postfix[''].append(k)
        if v not in postfix.keys(): postfix[v] = []
        postfix[v].append(k)

    ret = []
    eof = 0
    for prefix in postfix.keys():
        postfix[prefix], flag = tied_num(postfix[prefix])
        if flag: eof = 1
        if postfix[prefix] != '':
            ret.append(''.join([postfix[prefix], prefix]))

    rets = ','.join(ret)
    if len(ret) > 1: rets = ''.join(["{", rets, "}"])
    return rets, eof

def tied_num(nums):
    eof = 0
    rezn = re.compile("^0\d+")
    ren = re.compile("\d+")
    znum = {}
    num = []
    ret = []
    for i in nums:
        if i == '':
            eof = 1
        elif rezn.match(i):
            if len(i) not in znum.keys(): znum[len(i)] = []
            znum[len(i)].append(i)
        elif ren.match(i):
            num.append(int(i))
        else:
            ret.append(i)

    if len(num) > 0:
        num.sort()
        pair = [0, 0]
        pair[0] = pair[1] = num[0]
        num.pop(0)
        for i in num:
            if i == pair[1] + 1:
                pair[1] += 1
            else:
                if pair[0] == pair[1]:
                    ret.append(str(pair[0]))
                else:
                    ret.append(str(pair[0]) + '~' + str(pair[1]))
                pair[0] = pair[1] = i
        if pair[0] == pair[1]:
            ret.append(str(pair[0]))
        else:
            ret.append(str(pair[0]) + '~' + str(pair[1]))

    for i in znum.values():
        i.sort()
        pair = [0, 0]
        l = len(i[0])
        pair[0] = pair[1] = int(i[0])
        i.pop(0)
        for j in i:
            if int(j) == pair[1] + 1:
                pair[1] += 1
            else:
                if pair[0] == pair[1]:
                    ret.append('0' * (l - len(str(pair[0]))), str(pair[0]))
                else:
                    ret.append('0' * (l - len(str(pair[0]))) + str(pair[0]) + '~' \
                         + '0' * (l - len(str(pair[1]))) + str(pair[1]))
                pair[0] = pair[1] = int(j)

        if pair[0] == pair[1]:
            ret.append('0' * (l - len(str(pair[0]))), str(pair[0]))
        else:
            ret.append('0' * (l - len(str(pair[0]))) + str(pair[0]) + '~' \
                + '0' * (l - len(str(pair[1]))) + str(pair[1]))

    rets = ','.join(ret)
    if len(ret) > 1: rets = ''.join(["{", rets, "}"])
    return rets, eof
