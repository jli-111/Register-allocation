import liveness

class Graph:
  def __init__(self, local_vars):
    adjs = {}
    for var in local_vars:
      adjs[var] = set()
    self.adjs = adjs
    self.local_vars = local_vars

  def add_edge(self, from_, to_):
    if from_ in self.local_vars and to_ in self.local_vars and from_ != to_:
      old_from = self.adjs[from_] 
      old_from.add(to_)
      old_to = self.adjs[to_]
      old_to.add(from_)

  def neighbours(self, var):
    return self.adjs[var]
  
  def all_nodes(self):
    return self.local_vars
  
  def remove_node(self, var):
    del(self.adjs[var])
    self.local_vars.remove(var)
    for n in self.adjs:
      adjs = self.adjs[n]
      if var in adjs:
        adjs.remove(var)
  
  def print(self):
    for var in self.adjs:
      str = f"{var}: {self.adjs[var]}"
      print(str)

# Generate the interference graph
def process_block(graph, stmts, liveout):
  for stmt in reversed(stmts):
    for var1 in liveness.kill(stmt):
      for var2 in liveout:
        graph.add_edge(var1, var2)
    liveout = liveout.difference(liveness.kill(stmt)).union(liveness.gen(stmt))
  
def process_func(func):
  liveinfo = func.liveinfo
  for blk_label in func.blocks:
    liveout = liveness.compute_liveout(liveinfo, func.cfg, blk_label)
    blk_stmts = func.blocks[blk_label]
    process_block(func.igraph, blk_stmts, liveout)

def run(funcs):
  for func in funcs:
    process_func(func)
