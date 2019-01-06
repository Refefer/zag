from .graph import Graph
from .predicate import Predicate, All

class Workflow(object):
    def __init__(self):
        self.stages = {}
        self.graph = Graph()

    def add_stage(self, stage):
        if stage.name in self.stages:
            raise Exception("Stage {} already defined!")

        self.stages[stage.name] = stage
        self.graph.add_node(stage.name)
        for inbound in stage.depends_on:
            self.graph.add_edge(inbound, stage.name)

    def add_sequence(self, sequence):
        for stage in sequence.resolve_stages():
            self.add_stage()

    def get_ordered_stages(self, predicate=All()):
        assert isinstance(predicate, Predicate)
        for name in self.graph.toposort():
            stage = self.stages[name]
            if predicate.evaluate(stage):
                yield stage


