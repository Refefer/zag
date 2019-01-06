import re
import copy

from .configable import Configable, apply_config
from .stage import Stage, PyTask, ShellTask

class Sequence(Configable):
    def __init__(self, name, config=None, stages=(), depends_on=(), tags=()):
        self.name = name
        if config is None:
            config = {}

        self.config = config
        self.stages = stages
        self.depends_on = set(depends_on)
        self.tags = set(tags)

    def get_config(self):
        return self.config.copy()

    def apply_config(self, config):
        new_stages = []
        for stage in self.stages:
            stage_config = stage.get_config()
            stage_config.update(self.config)
            stage_config.update(config)
            new_stages.append(stage.apply_config(stage_config))

        tags = apply_config(self.tags, config)
        depends_on = apply_config(self.tags, config)
        return Sequence(self.name, {}, new_stages, depends_on, tags)
    
    def _get_stages(self):
        for stage in self.stages:
            if isinstance(stage, Sequence):
                for stage in stage.resolve_stages():
                    yield stage
            else:
                yield stage

    def resolve_stages(self):
        def _get_stages():
            for stage in self.stages:
                if isinstance(stage, Sequence):
                    for stage in stage.resolve_stages():
                        yield stage
                else:
                    yield stage

        for stage in _get_stages():
            stage.name = '{}/{}'.format(self.name, stage.name)
            stage.tags.update(self.tags)
            stage.tags.add(self.name)
            stage.depends_on.update(self.depends_on)
            yield stage
