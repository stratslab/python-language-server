# Copyright 2017 Palantir Technologies, Inc.
from pyflakes import api as pyflakes_api
from pyls import hookimpl, lsp


PYFLAKES_IGNORE_STATEMENT = '# pyflakes:ignore'


@hookimpl
def pyls_lint(document):
    reporter = PyflakesDiagnosticReport(document.lines)
    pyflakes_api.check(document.source, document.path, reporter=reporter)
    return reporter.diagnostics


class PyflakesDiagnosticReport(object):

    def __init__(self, lines):
        self.lines = lines
        self.diagnostics = []

    def unexpectedError(self, filename, msg):  # pragma: no cover
        pass

    def syntaxError(self, _filename, msg, lineno, offset, text):
        err_range = {
            'start': {'line': lineno - 1, 'character': offset},
            'end': {'line': lineno - 1, 'character': offset + len(text)},
        }
        self.diagnostics.append({
            'source': 'pyflakes',
            'range': err_range,
            'message': msg,
            'severity': lsp.DiagnosticSeverity.Error,
        })

    def flake(self, message):
        """ Get message like <filename>:<lineno>: <msg> """
        lno = message.lineno - 1
        if 0 <= lno < len(self.lines) and PYFLAKES_IGNORE_STATEMENT in self.lines[lno]:
            # don't report this error
            return

        err_range = {
            'start': {'line': lno, 'character': message.col},
            'end': {'line': lno, 'character': len(self.lines[lno])},
        }
        self.diagnostics.append({
            'source': 'pyflakes',
            'range': err_range,
            'message': message.message % message.message_args,
            'severity': lsp.DiagnosticSeverity.Warning
        })
