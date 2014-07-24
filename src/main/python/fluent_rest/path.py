"""
The module able to handle and manage a declared resource template path
"""

import re

from fluent_rest.exceptions import TypeUndefinedException


class Sort:
    """
    TODO
    """
    patterns = {}

    def __init__(self, sort):
        if sort not in Sort.patterns.keys():
            raise TypeUndefinedException(sort)

        self.__sort = sort

    def __str__(self):
        return self.__sort

    def __eq__(self, other):
        return isinstance(other, Sort) and self.form() == other.form()

    def form(self):
        return Sort.patterns[self.__sort]

    @staticmethod
    def define(name, form):
        re.compile(form)
        Sort.patterns[name] = form


class Var:
    """
    TODO
    """

    def __init__(self, name, sort=None):
        self.__name = name
        self.__sort = Sort(sort if sort is not None else "string")

    def name(self):
        return self.__name

    def sort(self):
        return self.__sort

    def regexp(self):
        return '(?P<%s>%s)' % (self.__name, self.__sort.form())

    def __eq__(self, other):
        return isinstance(other, Var) and \
               self.name() == other.name() and \
               self.sort() == other.sort()


class Path:
    """
    Path internal representation
    """

    def __init__(self, path):
        self.__path = path

    def path(self):
        return self.__path

    def matcher(self):
        def regexp(exp):
            if isinstance(exp, Var):
                return exp.regexp()
            else:
                return re.escape(exp)

        return '/'.join([regexp(p) for p in self.__path])

    def accept(self, path):
        match = re.match('^%s$' % self.matcher(), path)
        return None if match is None else match.groupdict()

    def __eq__(self, other):
        return isinstance(other, Path) and self.path() == other.path()

    @staticmethod
    def __parserItem(path):
        ident = Sort.patterns['ident']
        regexp = '^[{](?P<name>%s)(:(?P<sort>%s))?[}]$' % (ident, ident)

        result = re.match(regexp, path)
        if result is None:
            return path
        else:
            name = result.group('name')
            sort = result.group('sort')
            return Var(name, sort=sort)

    @staticmethod
    def parse(path):
        return Path([Path.__parserItem(p) for p in path.split('/')])

#
# Define native sorts
#

Sort.define('ident', '[a-zA-Z][a-zA-Z0-9]*')
Sort.define('string', '[^/]+')
Sort.define('int', '-?[0-9]+')
Sort.define('uuid',
            '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')
Sort.define('path', '.*')
