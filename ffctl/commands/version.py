import ffctl
from ffctl.commands.command_base import CommandBase


class VersionCmd(CommandBase):
    name = 'version'
    help_message = "Show client version"

    def __init__(self, options):
        super(VersionCmd, self).__init__(options)
        self.client_version = None

    @classmethod
    def _add_arguments(cls, parser):
        pass

    def _cli_version(self):
        return ffctl.__version__

    def _version(self):
        return {"version": self._cli_version()}

    def _call(self):
        pass

    def _render_dict(self):
        return self._version()

    def _render_console(self):
        return "\n".join(["%s: %s" % (k, v) for k, v in self._version().iteritems()])
