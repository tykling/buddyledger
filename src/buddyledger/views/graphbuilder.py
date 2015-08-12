#!/usr/bin/env python3
import functools
import itertools
from networkx import nx
from fractions import Fraction
from collections import defaultdict

def force_feasible(expenses, people):
    """ this adds an additional person that is involved in all expenses, which will often (if not always) make the problem feasible """
    newpeople = list(itertools.islice(filter(lambda x: x not in people, itertools.count(88888888)), 1))
    def fix(a):
        a.update({newpeople[0]: None})
        return a
    return wrapped([{"whopaid": expense["whopaid"], "whoshouldpay": fix(expense["whoshouldpay"])} for expense in expenses], newpeople + people)

def solve_mincost_problem_for_expenses(expenses, people, debug=False):
    if debug: print(expenses)
    nodes = defaultdict(lambda: 0)
    
    G = nx.DiGraph()
    for idx, expense in enumerate(expenses):
    
        whopaid = expense["whopaid"]
        whoshouldpay = expense["whoshouldpay"]
        #total = functools.reduce(lambda accu, that: that["amount"] + accu, whopaid, 0)
        total = sum(that["amount"] for that in whopaid)
    
        for v in people:
            if v in whoshouldpay:
                if whoshouldpay[v] is not None:
                    idealcontrib = whoshouldpay[v]
                else:
                    notnone = [x for x in whoshouldpay.values() if x is not None]
                    idealcontrib = Fraction(total - sum(notnone), len(whoshouldpay) - len(notnone))
            else:
                idealcontrib = 0
            actualcontrib = sum([w["amount"] for w in expense["whopaid"] if w["personId"] == v])
            diff = actualcontrib - idealcontrib
            #print(actualcontrib, idealcontrib, diff)
            nodes[v] += diff;
    
    for i, v in nodes.items():
        G.add_node(i, demand=v)
    
    G.add_weighted_edges_from(x + (1,) for x in itertools.permutations(people, 2))
    
    flowCost, flowDict = nx.network_simplex(G)
    return flowDict

if __name__ == "__main__":
    print(solve_mincost_problem_for_expenses([{"whopaid": [{"personId": 10, "amount": Fraction(1,2)}, {"personId": 11, "amount": Fraction(1,2)}], "whoshouldpay": {10: None, 11: None, 12: Fraction(1,2)}}] , [10,11,12], 1))
    # invalid problems (invalid constraint because all people contribute an amount which is unequal the paid amount:
    # from buddyledger.baconsvin.org/ledger/17
    print(solve_mincost_problem_for_expenses([{'whopaid': [{'personId': 60, 'amount': Fraction(1,2)}], 'whoshouldpay': {60: Fraction(1, 6), 61: None}}], [61, 60], 1))
    #                                                                                                                added to make feasible ^^^^^^^^
    print(solve_mincost_problem_for_expenses([{'whopaid': [{'personId': 60, 'amount': Fraction(1,2)}], 'whoshouldpay': {60: Fraction(1, 6)}}], [61, 60], 1)) # would make an error
    print(solve_mincost_problem_for_expenses([{'whopaid': [{'amount': Fraction(75, 1), 'personId': 60}], 'whoshouldpay': {60: Fraction(25, 1), 61: Fraction(25, 1)}}], [60,61], 1))
    print(solve_mincost_problem_for_expenses([{'whopaid': [{'amount': Fraction(3, 1), 'personId': 60}], 'whoshouldpay': {60: Fraction(1, 1), 61: Fraction(1, 1)}}], [61, 60], 1))
