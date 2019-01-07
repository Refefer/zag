import unittest

from zag.graph import *

class ConfigTest(unittest.TestCase):

    def test_toposort(self):
        edges = [
            ('a', 'b'),
            ('a', 'c'),
            ('d', 'b'),
            ('c', 'd')
        ]

        nodes = {n for ns in edges for n in ns}
        graph = Graph()
        for n in nodes:
            graph.add_node(n)

        for start, end in edges:
            graph.add_edge(start, end)

        order = list(graph.toposort())
        self.assert_(order.index('a') < order.index('d'))
        self.assert_(order.index('c') < order.index('d'))
        self.assert_(order.index('d') < order.index('b'))

if __name__ == '__main__':
    unittest.main()
