import unittest

from zag import *
from zag.configable import ConfigException

class ConfigTest(unittest.TestCase):

    def test_stage(self):
        foo = PyTask("zag.foo")

        workflow = Sequence("foo-flow", stages=[
            Stage("run-foo",
                foo,
                args=[
                    ("--foo-type", "$type")
                ])
        ])

        self.assertEqual(workflow.get_config(), {})

        my_config = {"type": "ponies"}

        nw = workflow.apply_config(my_config)

        self.assertEqual(nw.stages[0].args, [("--foo-type", "ponies")])

    def test_missing_value(self):
        foo = PyTask("zag.foo")

        workflow = Sequence("foo-flow", stages=[
            Stage("run-foo",
                foo,
                args=[
                    ("--foo-type", "$type"),
                    ("--missing-val", "$mv")
                ])
        ])

        self.assertEqual(workflow.get_config(), {})

        my_config = {"type": "ponies"}

        with self.assertRaises(ConfigException):
            nw = workflow.apply_config(my_config)

    def test_nested_workflows(self):
        foo = PyTask("zag.foo")

        simple_stage = Stage("run-foo",
            foo,
            args=[
                ("--foo-type", "$type")
            ])

        bar = Sequence('bar-flow',
            config={
                "type": "bar"
            },
            stages=[simple_stage])

        baz = Sequence('baz-flow',
            config={
                "type": "baz"
            },
            stages=[simple_stage])

        qux = Sequence('qux-flow',
            config={
                "type": "qux"
            },
            stages=[baz])

        workflow = Sequence("all-workflows", stages=[
            bar,
            qux,
            baz
        ])

        config = {}
        nw = workflow.apply_config(config)

        self.assertEqual(nw.stages[0].stages[0].args, [("--foo-type", "bar")])
        self.assertEqual(nw.stages[1].stages[0].stages[0].args, [("--foo-type", "qux")])
        self.assertEqual(nw.stages[2].stages[0].args, [("--foo-type", "baz")])

    def test_tags(self):
        simple_stage = Stage("run-foo",
            PyTask("zag.foo"),
            args=[
                ("--foo-type", "$type")
            ],
            tags=['$tag'])

        baz = Sequence('baz-flow',
            config={
                "type": "baz"
            },
            stages=[simple_stage],
            tags=["fomo"])

        with self.assertRaises(ConfigException):
            baz.apply_config({})

        nw = baz.apply_config({"tag": "TAG"})
        self.assertEqual(nw.stages[0].tags, {"TAG"})

    def test_inherit_tags(self):
        simple_stage = Stage("run-foo",
            PyTask("zag.foo"),
            args=[
                ("--foo-type", "$type")
            ],
            tags=['foo'])

        baz = Sequence('baz-flow',
            config={
                "type": "baz"
            },
            stages=[simple_stage],
            tags=['all-baz'])

        stages = baz.apply_config({"tag": "TAG"}).resolve_stages()
        stages = list(stages)
        self.assertEqual(stages[0].tags, {"foo", "baz-flow", "all-baz"})

class ZagTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_identity(self):
        pass
    
if __name__ == '__main__':
    unittest.main()
