#curl --header "Content-Type: application/json" https://gitlab.example.com/api/v4/ci/lint --data '{"content": "{ \"image\": \"ruby:2.1\", \"services\": [\"postgres\"], \"before_script\": [\"gem install bundler\", \"bundle install\", \"bundle exec rake db:create\"], \"variables\": {\"DB_NAME\": \"postgres\"}, \"types\": [\"test\", \"deploy\", \"notify\"], \"rspec\": { \"script\": \"rake spec\", \"tags\": [\"ruby\", \"postgres\"], \"only\": [\"branches\"]}}"}'
import json
import yaml
import requests
from ffctl.commands.command_base import CommandBase, LoadVariables


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
        self.result = ''

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument("-H", "--host", help="gitlab host", default="https://gitlab.com")
        parser.add_argument('filepath', nargs='?', default=[".gitlab-ci.yml"], help="lint file to render")

    def _call(self):
        path = "%s/%s" % (self.host, "api/v4/ci/lint")
        with open(self.filepath, 'r') as filepath:
            resp = requests.post(path, json={'content': filepath.read()})
            result = resp.json()
            if 'status' not in result or result['status'] != 'valid':
                self.result = resp.json()

    def _render_dict(self):
        return self.result

    def _render_console(self):
        return self.result
