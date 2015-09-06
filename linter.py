#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Joe Bateson
# Copyright (c) 2015 Joe Bateson
#
# License: MIT
#

"""This module exports the CheetahFlake plugin class."""

import re

from SublimeLinter.lint import PythonLinter, util


class CheetahFlake(PythonLinter):

    """Provides an interface to cheetah-flake."""

    syntax = 'yelpcheetah'
    cmd = ('cheetah-flake@python', '@')
    version_requirement = None
    regex = (
        r'^.+?:(?P<line>\d+)\s'
        r'((?:(?P<error>[E]))|(?:(?P<warning>[WF])))\d+\s'
        r'(?P<message>.*((?P<near>\'.+\').*)|(.*))$'
        r'|(?P<fail>^Traceback.*)'
    )
    fail_re = re.compile((
        r'.*\n(?P<message>.+?(?P<near>".*")?.*)\n+'
        r'Line (?P<line>\d+), column (?P<col>\d+)'
    ), re.DOTALL)
    multiline = True
    line_col_base = (1, 1)
    tempfile_suffix = 'tmpl'
    error_stream = util.STREAM_BOTH
    check_version = False

    def split_match(self, match):
        """
        Extract and return values from match.

        We override this method so that we can handle compilation errors.
        """
        if match:
            fail = match.group('fail')

            if fail:
                fail_match = self.fail_re.match(match.string)
                match = fail_match or match

        return super().split_match(match)
