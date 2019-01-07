class Predicate(object):
    def evaluate(self, stage):
        raise NotImplementedError()

class AllTags(Predicate):
    def __init__(self, tags):
        assert isinstance(tags, (set,list,tuple))
        self.tags = set(tags)

    def evaluate(self, stage):
        return self.tags.issubset(stage.tags)

class AnyTags(Predicate):
    def __init__(self, tags):
        assert isinstance(tags, (set,list,tuple))
        self.tags = set(tags)

    def evaluate(self, stage):
        return len(self.tags & stage.tags) > 0

class StageNames(Predicate):
    def __init__(self, stages):
        self.stages = set(stages)

    def evaluate(self, stage):
        return stage.name in self.stages

class Not(Predicate):
    def __init__(self, p):
        assert isinstance(p, Predicate)
        self.p = p

    def evaluate(self, stage):
        return not self.p.evaluate(stage)

class All(Predicate):
    def evaluate(self, stage):
        return True

class And(Predicate):
    def __init__(self, preds):
        self.preds = preds

    def evaluate(self, stage):
        return all(p.evaluate(stage) for p in self.preds)

