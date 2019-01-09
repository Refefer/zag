import select
import os
import subprocess
import logging
import shlex
import imp

from .configable import Configable

class Task(Configable):
    pass

class PyTask(Task):
    def __init__(self, path, entrypoint='main', parser=None):
        self.path = path
        self.entrypoint = entrypoint
        self.parser = parser

    def __unicode__(self):
        return u"Python[Path=`{}`,Entrypoint=`{}`,parser=`{}`]".format(
                self.path, self.entrypoint, self.parser)

class ShellTask(Task):
    def __init__(self, script):
        self.script = script

    def __unicode__(self):
        return u"Shell[Script={}]".format(
                self.path, self.entrypoint, self.parser)

class Stage(Configable):
    def __init__(self, name, task, depends_on=(), args=(), tags=()):
        self.name = name
        self.task = task
        self.depends_on = set(depends_on)
        self.args = list(args)
        self.tags = set(tags)

    def _get_args(self):
        args = []
        for argset in self.args:
            for arg in argset:
                assert isinstance(arg, basestring)
                args.append(arg)

        return args

    def _run_pytask(self):
        pid = os.fork()
        if pid == 0:
            args = self._get_args()
            name = os.path.basename(self.task.path).split('.')[0]
            mod = imp.load_source(name, self.task.path)
            if self.task.parser is not None:
                m_args = getattr(mod, self.task.parser)().parse_args(args)
            else:
                m_args = [None] + args

            if not hasattr(mod, self.task.entrypoint):
                raise Exception("Entrypoint `{}` does not exist in `{}`!".format(
                    self.task.entrypoint, self.task.mod))

            getattr(mod, self.task.entrypoint)(m_args)
            os._exit(0)

        return os.waitpid(pid, 0)[1] == 0

    def _run_shelltask(self):
        args = shlex.split(self.task.script) + self._get_args()
        proc = subprocess.Popen(
            args,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE)

        while True:
            so = proc.stdout.fileno()
            ri, _, err = select.select([so], [], [so], 0.1)
            if ri: 
                x = proc.stdout.readline()
                if not x:
                    break

                logging.info("%s: %s", self.name, x.strip())

            elif err:
                break

        return proc.wait() == 0

    def run(self):
        if isinstance(self.task, PyTask):
            try:
                return self._run_pytask()
            except Exception:
                logging.exception("Error when running %s", self.name)
                return False

        else:
            return self._run_shelltask()

