import logging
import sys

from rope.base import libutils
from rope.refactor.extract import ExtractMethod, ExtractVariable

from pyls import hookimpl

log = logging.getLogger(__name__)


def pyls_extract(extract_obj, new_name, replace_similar, extract_as_global):
    changeset = extract_obj.get_changes(new_name, similar=replace_similar, global_=extract_as_global)
    log.debug("Finished extraction: %s", changeset.changes)
    return {
        'edits': [{
            'range': {
                'start': {'line': 0, 'character': 0},
                'end': {'line': sys.maxsize, 'character': 0},
            },
            'newText': change.new_contents
        } for change in changeset.changes]
    }


@hookimpl
def pyls_extract_method(workspace, document, range, new_name, replace_similar, extract_as_global):
    extract_method = ExtractMethod(
        workspace._rope,
        libutils.path_to_resource(workspace._rope, document.path),
        document.offset_at_position(range['start']),
        document.offset_at_position(range['end'])
    )

    log.debug("Executing extract method in document %s with new name %s", document.path, new_name)
    return pyls_extract(extract_method, new_name, replace_similar, extract_as_global)


@hookimpl
def pyls_extract_variable(workspace, document, range, new_name, replace_similar, extract_as_global):
    extract_variable = ExtractVariable(
        workspace._rope,
        libutils.path_to_resource(workspace._rope, document.path),
        document.offset_at_position(range['start']),
        document.offset_at_position(range['end'])
    )

    log.debug("Executing extract variable in document %s with new name %s", document.path, new_name)
    return pyls_extract(extract_variable, new_name, replace_similar, extract_as_global)
