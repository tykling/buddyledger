#!/usr/bin/env python3
import functools
import itertools
from networkx import nx
from fractions import Fraction
from collections import defaultdict

def solve_mincost_problem_for_expenses(expenses, people):
    nodes = defaultdict(lambda: 0)
    
    G = nx.DiGraph()
    for expense in expenses:
    
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
    expenses = [{"whopaid": [{"personId": 10, "amount": Fraction(1,2)},
        {"personId": 11, "amount": Fraction(1,2)}
        ], "whoshouldpay": {10: None, 11: None, 12: Fraction(1,2)}}]
    print(expenses)
    print(solve_mincost_problem_for_expenses(expenses, [10,11,12]))
