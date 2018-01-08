import unittest
import numpy as np
import pandas as pd
import graphviz as gv

def is_terminal(string, Vt):
    if len(string) == 1 and string in Vt:
        return True
    else:
        return False

def is_nonterminal(string, Vn):
    if len(string) == 1 and string in Vn:
        return True
    else:
        return False

def is_rule_type3(string, Vt, Vn):
    if len(string) == 2:
        if (is_terminal(string[0], Vt) and is_nonterminal(string[0]), Vn) or\
                (is_nonterminal(string[0], Vn) and is_terminal(string[1]), Vt):
            return True
        else:
            return False
    if len(string) == 1 and is_terminal(string, Vt):
        return True
    return False


def is_type3(P, Vt, Vn):
    if all([ is_nonterminal(i, Vn) for i in P.keys()]) and \
            all([all([ is_rule_type3(rule, Vt, Vn) for rule in rules]) for rules in P.values()]) :
        return True
    else:
        return False

def is_type2(P, Vn):
    if all ([is_nonterminal (i, Vn) for i in P.keys ()]):
        return True
    else:
        return False




def is_type1(P):
    if all([all([ len(i) >= len(key) for i in P[key] ]) for key in P]):
        return True
    else:
        return False

def define_grammar_type(P, Vt, Vn):
    if not is_type3(P, Vt, Vn):
        if not is_type2(P,Vn):
            if not is_type1(P):
                return 'type0'
            else:
                return 'type1'
        else:
            return 'type2'
    else:
        return 'type3'

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


class Test (unittest.TestCase):
    # S -> aSBC | abc
    # bCBCC -> bc
    # CBa -> BC
    # cC -> cc

    def test_type0 ( self ):
        Vt = ['a', 'b', 'c']
        Vn = ['S', 'C', 'B']
        P = {'S': ['aSBC', 'abc'], 'bCBCC': ['bc'], 'CBa': ['BC'], 'cC': ['cc']}
        self.assertEqual(define_grammar_type(P, Vt, Vn), 'type0')

    # S -> aSBC | abc
    # bC -> bc
    # CB -> BC
    # cC -> cc

    def test_type1 ( self ):
        Vt = ['a', 'b', 'c']
        Vn = ['S', 'C', 'B']
        P = {'S': ['aSBC', 'abc'], 'bC': ['bc'], 'CB': ['BC'], 'cC': ['cc']}
        self.assertEqual(define_grammar_type(P, Vt, Vn), 'type1')

    # S -> aQb | accb
    # Q -> cSc

    def test_type2 ( self ):
        Vt = ['a', 'b', 'c']
        Vn = ['Q', 'S']
        P = {'S': ['aQb', 'accb'], 'Q': ['cSc']}
        self.assertEqual(define_grammar_type(P, Vt, Vn), 'type2')

    # S -> A& | B&
    # A -> a | Ba
    # B -> b | Bb | Ab

    def test_type3 ( self ):
        Vt = ['a', 'b', '&']
        Vn = ['A', 'B', 'S']
        P = {'S': ['A&', 'B&'], 'A': ['a', 'Ba'], 'B': ['b', 'Bb', 'Ab']}
        self.assertEqual(define_grammar_type(P, Vt, Vn), 'type3')

    # S -> Aa | Ab
    # A -> Bc
    # B -> Ca | Cb
    # C -> Dc
    # D -> a | b

    def test_my_grammar(self):
        Vt = ['a', 'b', 'c']
        Vn = ['S', 'A', 'B', 'C', 'D']
        P = { 'S' : ['Aa', 'Ab'], 'A' : ['Bc'], 'B' : ['Ca', 'Cb'], 'C' : ['Dc'], 'D' : ['a', 'b']}
        self.assertEqual(define_grammar_type(P, Vt, Vn), "type3")


    def test_fsm(self):
        Vt = ['X', 'Y', 'Z', 'W', 'V']
        Vn = ['0', '1', '~', '#', '&']
        P = {
            'X': ['0Y', '1Z', 'e'],
            'Y': ['0', 'Z', '~W', '#'],
            'Z': ['1Y', '1W', '0V'],
            'W': ['0W', '1W', '#'],
            'V': ['&Z']
        }

        for i in P:
            P[i] = [ j + 'N'  if len(j) == 1 and j in Vn else j  for j in P[i] ]

        Pt = P



        table = []
        for i in Vn:
            for key in Pt:
                table.append({ key : [ j.strip(i) if i in j else None  for j in Pt[key]] })

        result = {}
        for i in Vt:
            t = filter(lambda x: x.keys()[0] == i , table)
            t = { t[0].keys()[0] : [ filter(lambda x: x != None , j[i]) for j in t] }
            result.update(t)

        fsm = pd.DataFrame(data=result)
        fsm = fsm.rename_axis(lambda x: Vn[x])
        g1 = gv.Graph(format='svg')

        print fsm
       # print np.array(table)


if __name__ == '__main__':
    unittest.main()







