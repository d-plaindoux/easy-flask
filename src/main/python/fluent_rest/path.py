'''
The module able to handle and manage a declared resource template path
'''

import re

# Path grammar
# ------------
#
# path ::= item
#        | item ('/' item)*
#
# item ::= string - { '/', '{', '}' }
#        | '{' IDENT (':' IDENT)? '}'
#

typeVar = {
    'ident': '[a-zA-Z][a-zA-Z0-9]*',
    'string': '[^/]+',
    'int': '-?[0-9]+',
    'path': '.*'
}


class Var:
    """
    TODO
    """

    def __init__(self, name, sort=None):
        self.__name = name
        self.__sort = sort if sort is not None else "string"

    def name(self):
        return self.__name

    def sort(self):
        return self.__sort

    def __str__(self):
        return '(?P<%s>%s)' % (self.__name, typeVar[self.__sort])

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

    def accept(self, path):
        matcher = '/'.join([str(p) for p in self.__path])
        return re.match('^%s$' % matcher, path)

    def __eq__(self, other):
        return isinstance(other, Path) and self.path() == other.path()

    @staticmethod
    def __parserItem(path):
        ident = typeVar['ident']
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
