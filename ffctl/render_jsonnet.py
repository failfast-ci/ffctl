import json
import logging
import os
import os.path
import re

import _jsonnet

import ffctl.template_filters as filters

logger = logging.getLogger(__name__)


class RenderJsonnet(object):
    def __init__(self, files=None, manifestpath=None, lib_dirs=[]):
        self.manifestdir = None
        if manifestpath:
            self.manifestdir = os.path.dirname(manifestpath)
        self.files = files
        lib_dirs.append(os.path.join(os.path.dirname(__file__), "jsonnet/lib"))
        self.lib_dirs = lib_dirs

    #  Returns content if worked, None if file not found, or throws an exception
    def try_path(self, path, rel):
        if rel[0] == '/':
            full_path = rel
        else:
            full_path = path + rel

        if full_path[-1] == '/':
            raise RuntimeError('Attempted to import a directory')

        if not rel:
            raise RuntimeError('Got invalid filename (empty string).')
        if self.files is not None and full_path in self.files:
            if self.files[full_path] is None:
                with open(full_path) as f:
                    self.files[full_path] = f.read()
            return rel, self.files[full_path]

        # @TODO(ant31) fail if full_path is absolute
        elif self.manifestdir and os.path.isfile(os.path.join(self.manifestdir, full_path)):
            filepath = os.path.join(self.manifestdir, full_path)
            with open(filepath) as f:
                return rel, f.read()
        else:
            for libdir in self.lib_dirs:
                libpath = os.path.join(libdir, rel)
                if os.path.isfile(libpath):
                    with open(libpath) as f:
                        return rel, f.read()

        if not os.path.isfile(full_path):
            return full_path, None

        with open(full_path) as f:
            return full_path, f.read()

    def import_callback(self, path, rel):
        full_path, content = self.try_path(path, rel)
        if content:
            return full_path, content
        raise RuntimeError('File not found')

    def render_jsonnet(self, manifeststr, tla_codes=None):
        # @TODO(ant31): workaround until jsonnet compile on windows
        import _jsonnet
        try:
            json_str = _jsonnet.evaluate_snippet(  # pylint: disable=no-member
                "snippet", manifeststr, import_callback=self.import_callback,
                native_callbacks=filters.jsonnet_callbacks(), tla_codes=tla_codes)

        except RuntimeError as e:
            print("tla_codes: %s" % (str(tla_codes)))
            print("\n".join([
                "%s %s" % (i, line) for i, line in enumerate([
                    l for l in manifeststr.split("\n") if re.match(r"^ *#", l) is None])]))
            raise e
        return json.loads(json_str)
