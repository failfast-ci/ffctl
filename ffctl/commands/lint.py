import requests
from ffctl.commands.command_base import CommandBase


def gitlab_lint(host, data):
    path = "%s/%s" % (host, "api/v4/ci/lint")
    resp = requests.post(path, json={'content': data})
    return resp.json()


def lint_status(resp):
    if 'status' not in resp or resp['status'] != 'valid':
        return False
    return True


class LintCmd(CommandBase):
    name = 'lint'
    help_message = "Lint the .gitlab-ci.yml"

    def __init__(self, options):
        super(LintCmd, self).__init__(options)
        self.host = options.host
        if isinstance(options.filepath, list):
            self.filepath = options.filepath[0]
        else:
            self.filepath = options.filepath
        self.output = "yaml"

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument("-H", "--host", help="gitlab host", default="https://gitlab.com")
        parser.add_argument('filepath', nargs='?', default=[".gitlab-ci.yml"], help="lint file to render")

    def _call(self):
        with open(self.filepath, 'r') as filepath:
            resp = gitlab_lint(self.host, filepath.read())
            self.result = resp

    def _render_dict(self):
        return self.result

    def _render_console(self):
        return self.result
