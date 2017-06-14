#!/usr/bin/env python
import argparse
import os

from ffctl.commands.command_base import CommandBase, LoadVariables
from ffctl.commands.jsonnet import JsonnetCmd
from ffctl.commands.version import VersionCmd
from ffctl.commands.lint import LintCmd


def all_commands():
    base_cmd = {}
    for cmd in base_cmd.values():
        cmd.__bases__ = (CommandBase,)

    base_cmd.update({
        VersionCmd: VersionCmd,
        JsonnetCmd.name: JsonnetCmd,
        LintCmd.name: LintCmd,
    })
    return base_cmd


def get_parser(commands):
    parser = argparse.ArgumentParser()
    # JsonnetCmd._add_output_option(parser)
    # JsonnetCmd._add_arguments(parser)

    # parser.set_defaults(func=JsonnetCmd.call, which_cmd=JsonnetCmd.name, parse_unknown=JsonnetCmd.parse_unknown)

    subparsers = parser.add_subparsers(help='command help')

    for command_class in commands.values():
        command_class.add_parser(subparsers)
    return parser


def cli():
    try:
        parser = get_parser(all_commands())
        unknown = None
        args, unknown = parser.parse_known_args()
        if args.parse_unknown:
            args.func(args, unknown)
        else:
            args = parser.parse_args()
            args.func(args)

    except (argparse.ArgumentTypeError, argparse.ArgumentError) as exc:
        if os.getenv("FFLINTER_DEBUG", "false") == "true":
            raise
        else:
            print exc.message
            #parser.error(exc.message)
