from collections import defaultdict, deque
class Graph(object):
    def __init__(self):
        self.nodes = {}
        self.inbound = defaultdict(set)
        self.outbound = defaultdict(set)

    def add_node(self, name):
        if name in self.nodes:
            raise TypeError("Node {} already exists in graph!".format(name))

        self.nodes[name] = name

    def add_edge(self, start, end):
        ns = self.nodes[start]
        ne = self.nodes[end]
        self.inbound[ne].add(ns)
        self.outbound[ns].add(ne)

    def toposort(self):
        stack = deque([name for name, idx in self.nodes.items() if idx not in self.inbound])
        inbound = {k: set(vs) for k, vs in self.inbound.items()}
        while stack:
            node = stack.popleft()
            yield node
            for out_node in self.outbound[node]:
                inbound[out_node].remove(node)
                if len(inbound[out_node]) == 0:
                    stack.append(out_node)
        
