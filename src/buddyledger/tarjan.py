from collections import namedtuple

TarjanContext = namedtuple('TarjanContext', ['g', 'S','S_set', 'index', 'lowlink',  'T','ret'])

def _tarjan_head(ctx, v):
        """ Used by @tarjan and @tarjan_iter.  This is the head of the
            main iteration """
        ctx.index[v] = len(ctx.index)
        ctx.lowlink[v] = ctx.index[v]
        ctx.S.append(v)
        ctx.S_set.add(v)
        it = iter(ctx.g.get(v, ()))
        ctx.T.append((it,False,v,None))

def _tarjan_body(ctx, it, v):
        """ Used by @tarjan and @tarjan_iter.  This is the body of the
            main iteration """
        for w in it:
                if w not in ctx.index:
                        ctx.T.append((it,True,v,w))
                        _tarjan_head(ctx, w)
                        return
                if w in ctx.S_set:
                        ctx.lowlink[v] = min(ctx.lowlink[v], ctx.index[w])
        if ctx.lowlink[v] == ctx.index[v]:
                scc = []
                w = None
                while v != w:
                        w = ctx.S.pop()
                        scc.append(w)
                        ctx.S_set.remove(w)
                ctx.ret.append(scc)

def tarjan(g):
        """ Returns the strongly connected components of the graph @g
            in a topological order.

                @g is the graph represented as a dictionary
                        { <vertex> : <successors of vertex> }.
        
            This function does not recurse. """
        ctx = TarjanContext(
                g = g,
                S = [],
                S_set = set(),
                index = {},
                lowlink = {},
                T = [],
                ret = [])
        main_iter = iter(g)
        while True:
                try:
                        v = next(main_iter)
                except StopIteration:
                        return ctx.ret
                if v not in ctx.index:
                        _tarjan_head(ctx, v)
                while ctx.T:
                        it, inside, v, w = ctx.T.pop()
                        if inside:
                                ctx.lowlink[v] = min(ctx.lowlink[w],
                                                        ctx.lowlink[v])
                        _tarjan_body(ctx, it, v)

