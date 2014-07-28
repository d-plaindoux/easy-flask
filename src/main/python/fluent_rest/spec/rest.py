"""
The module able to decorate code for service specification
"""

from fluent_rest.spec.specification import Specification


def specs(function):
    return Specification.get(function)


def specsExists(function):
    return Specification.exists(function)


def Path(path):
    return Specification.getAndDefine(lambda s: s.Path(path))


def Verb(name):
    return Specification.getAndDefine(lambda s: s.Verb(name))


def Consumes(mime):
    return Specification.getAndDefine(lambda s: s.Consumes(mime))


def Produces(mime):
    return Specification.getAndDefine(lambda s: s.Produces(mime))


GET = Verb('GET')
PUT = Verb('PUT')
POST = Verb('POST')
DELETE = Verb('DELETE')

