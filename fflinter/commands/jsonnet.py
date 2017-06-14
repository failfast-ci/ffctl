import yaml
from fflinter.render_jsonnet import RenderJsonnet
from fflinter.commands.command_base import CommandBase, LoadVariables


class JsonnetCmd(CommandBase):
    name = 'jsonnet'
    help_message = "Resolve a jsonnet file with the fflinterstd available"

    def __init__(self, options):
        super(JsonnetCmd, self).__init__(options)
        self.variables = options.variables
        if isinstance(options.filepath, list):
            self.filepath = options.filepath[0]
        else:
            self.filepath = options.filepath
        self.result = None

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument("-x", "--variables", help="variables", default={}, action=LoadVariables)
        parser.add_argument('filepath', nargs='?', default=[".gitlab-ci.jsonnet"], help="jsonnet file to render")

    def _call(self):
        r = RenderJsonnet(manifestpath=self.filepath)
        tla_codes = self.variables
        p = open(self.filepath).read()
        self.result = r.render_jsonnet(p, tla_codes=tla_codes)

    def _render_dict(self):
        return self.result

    def _render_console(self):
        return yaml.safe_dump(self._render_dict(), default_flow_style=False, indent=2, width=200)
