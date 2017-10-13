import ffctl
from pyjsonnet.commands.version import VersionCmd as JVersionCommand


class VersionCmd(JVersionCommand):

    def _cli_version(self):
        return ffctl.__version__
