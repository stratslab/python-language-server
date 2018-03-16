# Copyright 2017 Palantir Technologies, Inc.
import pycodestyle
from pyls._utils import find_parents
from .source import ConfigSource


CONFIG_KEY = 'pycodestyle'
USER_CONFIGS = [pycodestyle.USER_CONFIG] if pycodestyle.USER_CONFIG else []
PROJECT_CONFIGS = ['pycodestyle.cfg', 'setup.cfg', 'tox.ini']

OPTIONS = [
    ('exclude', 'plugins.pycodestyle.exclude', list),
    ('filename', 'plugins.pycodestyle.filename', list),
    ('hang-closing', 'plugins.pycodestyle.hangClosing', bool),
    ('ignore', 'plugins.pycodestyle.ignore', list),
    ('max-line-length', 'plugins.pycodestyle.maxLineLength', int),
    ('select', 'plugins.pycodestyle.select', list),
]


class PyCodeStyleConfig(ConfigSource):

    def user_config(self):
        print("PyCodeStyleConfig: user config ")
        config = self.read_config_from_files(USER_CONFIGS)
        res = self.parse_config(config, CONFIG_KEY, OPTIONS)
        print("Res = ", res)
        return res

    def project_config(self, document_path):
        print("PyCodeStyleConfig: project config ")
        files = find_parents(self.root_path, document_path, PROJECT_CONFIGS)
        config = self.read_config_from_files(files)
        res = self.parse_config(config, CONFIG_KEY, OPTIONS)
        print("Res = %s", res)
        return res
