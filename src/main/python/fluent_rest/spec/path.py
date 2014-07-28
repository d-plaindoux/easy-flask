"""
The module able to handle and manage a declared resource template path
"""

from re import match
from re import escape
from re import compile
from uuid import UUID
from fluent_rest.exceptions import TypeUndefinedException
from fluent_rest.exceptions import VariableUndefinedException


class Sort:
    """
    TODO
    """
    patterns = {}
    converts = {}

    def __init__(self, sort):
        if sort not in Sort.patterns.keys():
            raise TypeUndefinedException(sort)

        self.__sort = sort

    def __str__(self):
        return self.__sort

    def __eq__(self, other):
        return isinstance(other, Sort) and self.pattern() == other.pattern()

    def pattern(self):
        return Sort.patterns[self.__sort]

    def convert(self):
        return Sort.converts[self.__sort]

    @staticmethod
    def define(name, form, decode=(lambda f: f)):
        compile(form)
        Sort.patterns[name] = form
        Sort.converts[name] = decode


class Var:
    """
    TODO
    """

    def __init__(self, name, sort=None):
        self.__name = name
        self.__sort = Sort('string' if sort is None else sort)

    def name(self):
        """
        Return the variable name
        """
        return self.__name

    def sort(self):
        """
        Return the variable sort (type)
        """
        return self.__sort

    def regexp(self):
        """
        Return the variable regular expression
        """
        return '(?P<%s>%s)' % (self.__name, self.__sort.pattern())

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
                return escape(exp)

        return '/'.join([regexp(p) for p in self.__path])

    def __variables(self):
        return [p for p in self.__path if isinstance(p, Var)]

    def __variable(self, name):
        try:
            return (p for p in self.__variables() if p.name() == name).next()
        except StopIteration, _:
            raise VariableUndefinedException(name)

    def __convert(self, name, value):
        return self.__variable(name).sort().convert()(value)

    def accept(self, path):
        matched = match('^%s$' % self.matcher(), path)
        return None if matched is None \
            else lambda n: self.__convert(n, matched.group(n))

    def __eq__(self, other):
        return isinstance(other, Path) and self.path() == other.path()

    @staticmethod
    def __parserItem(path):
        ident = Sort.patterns['ident']
        regexp = '^[{](?P<name>%s)(:(?P<sort>%s))?[}]$' % (ident, ident)

        result = match(regexp, path)
        if result is None:
            return path
        else:
            return Var(result.group('name'), result.group('sort'))

    @staticmethod
    def parse(path):
        return Path([Path.__parserItem(p) for p in path.split('/')])

#
# Define native sorts with corresponding converter.
# Note: No converter stands for as-is string value
#

Sort.define('ident', '[a-zA-Z][a-zA-Z0-9]*')
Sort.define('string', '[^/]+')
Sort.define('int', '[-+]?[0-9]+', int)
Sort.define('float', '[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?', float)
Sort.define('uuid', '[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}', UUID)
Sort.define('path', '.+')
