# Copyright (C)2014 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

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


def Provider(kind):
    return Specification.getAndDefine(lambda s: s.Provider(kind))


def Inject(kind):
    return Specification.getAndDefine(lambda s: s.Inject(kind))

PUT = Verb('PUT')
POST = Verb('POST')

GET = Verb('GET')
DELETE = Verb('DELETE')
