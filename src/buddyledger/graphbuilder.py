#!/usr/bin/env python3
import functools
import itertools
from networkx import nx
from fractions import Fraction

def getpersonscontributedamount(whopaid, personId):
    return sum([v["amount"] for v in whopaid if v["personId"] == personId])

def solve_mincost_problem_for_expenses(expenses, numPeople):
    nodes = [] # b cx cy
    for person in range(numPeople):
        nodes.append({"b": 0})
    
    G = nx.DiGraph()
    edges = [] # from to C L U
    for expense in expenses:
    
        whopaid = expense["whopaid"]
        whoshouldpay = expense["whoshouldpay"]
        total = functools.reduce(lambda accu, that: that["amount"] + accu, whopaid, 0)
    
        for v in range(len(nodes)):
            idealcontrib = Fraction(total , len(whoshouldpay)) if v in whoshouldpay else 0
            actualcontrib = getpersonscontributedamount(expense["whopaid"],v)
            diff = actualcontrib - idealcontrib
            #print(actualcontrib, idealcontrib, diff)
            nodes[v]["b"] += diff;

    for v, i in zip(nodes, itertools.count()):
        #print(job["people"][i], v["b"])
        #G.add_node(job["people"][i], demand=v["b"])
        G.add_node(i, demand=v["b"])
    
    for i in range(numPeople):
        for j in range(numPeople):
            if (i != j):
                #G.add_weighted_edges_from([(job["people"][i], job["people"][j], 1)])
                G.add_weighted_edges_from([(i, j, 1)])

    #print(G)
    flowCost, flowDict = nx.network_simplex(G)
    return flowDict

if __name__ == "__main__":
    expenses = [{"whopaid": [{"personId": 0, "amount": Fraction(1,2)},
        {"personId": 1, "amount": Fraction(1,2)}
        ], "whoshouldpay": [0,1,2]}]
    print(solve_mincost_problem_for_expenses(expenses, 6))
