from __future__ import print_function
import argparse
import json
import re
import os
import copy

import yaml

from ffctl.render_jsonnet import RenderJsonnet


class CommandBase(object):
    name = 'command-base'
    help_message = 'describe the command'
    parse_unknown = False

    def __init__(self, args_options):
        self.args_options = args_options
        self.output = args_options.output

    def render(self):
        if self.output == 'none':
            return
        elif self.output == 'json':
            self._render_json()
        elif self.output == 'yaml':
            self._render_yaml()
        else:
            print(self._render_console())

    @classmethod
    def call(cls, options):
        cls(options)()

    def __call__(self):
        self._call()
        self.render()

    @classmethod
    def add_parser(cls, subparsers):
        parser = subparsers.add_parser(cls.name, help=cls.help_message)
        cls._add_output_option(parser)
        cls._add_arguments(parser)
        parser.set_defaults(func=cls.call, which_cmd=cls.name, parse_unknown=cls.parse_unknown)

    def _render_json(self):
        print(json.dumps(self._render_dict(), indent=2, separators=(',', ': ')))

    def _render_dict(self):
        raise NotImplementedError

    def _render_console(self):
        raise NotImplementedError

    def _render_yaml(self):
        print(yaml.safe_dump(self._render_dict(), default_flow_style=False))

    def _call(self):
        raise NotImplementedError

    @classmethod
    def _add_arguments(cls, parser):
        raise NotImplementedError

    @classmethod
    def _add_registryhost_option(cls, parser):
        parser.add_argument("-H", "--registry-host",
                            default=None,
                            help=argparse.SUPPRESS)

    @classmethod
    def _add_output_option(cls, parser):
        parser.add_argument("--output", default="text", choices=['text',
                                                                 'none',
                                                                 'json',
                                                                 'yaml'],
                            help="output format")


class LoadVariables(argparse.Action):

    def _parse_cmd(self, var):
        r = {}
        try:
            return json.loads(var)
        except:
            for v in var.split(","):
                sp = re.match("(.+?)=(.+)", v)
                if sp is None:
                    raise ValueError("Malformed variable: %s" % v)
                key, value = sp.group(1), sp.group(2)
                r[key] = value
        return r

    def _load_from_file(self, filename, ext):
        with open(filename, 'r') as f:
            if ext in ['.yml', '.yaml']:
                return yaml.load(f.read())
            elif ext == '.json':
                return json.loads(f.read())
            elif ext in [".jsonnet", "libjsonnet"]:
                r = RenderJsonnet()
                return r.render_jsonnet(f.read())
            else:
                raise ValueError("File extension is not in [yaml, json, jsonnet]: %s" % filename)

    def load_variables(self, var):
        _, ext = os.path.splitext(var)
        if ext not in ['.yaml', '.yml', '.json', '.jsonnet']:
            return self._parse_cmd(var)
        else:
            return self._load_from_file(var, ext)

    def __call__(self, parser, namespace, values, option_string=None):
        items = copy.copy(argparse._ensure_value(namespace, self.dest, {}))
        try:
            items.update(self.load_variables(values))
        except ValueError as e:
            raise parser.error(option_string + ": " + e.message)
        setattr(namespace, self.dest, items)
