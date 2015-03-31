# Copyright (C)2015 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

from fluent_rest.spec.specification import Specification


def returnParam(f):
    def fun(e):
        f(e)
        return e

    return fun


def specification(function):
    return Specification.get(function)


def specificationExists(function):
    return Specification.exists(function)


def Path(path):
    return returnParam(lambda e: Specification.get(e).Path(path))


def Verb(name):
    return returnParam(lambda e: Specification.get(e).Verb(name))


def Consumes(mime, transducer=None):
    return returnParam(
        lambda e: Specification.get(e).Consumes(mime, transducer)
    )


def Produces(mime, transducer=None):
    return returnParam(
        lambda e: Specification.get(e).Produces(mime, transducer)
    )


def Provider(aType):
    return returnParam(lambda e: Specification.get(e).Provider(aType))


def Inject(aType):
    return returnParam(lambda e: e)


#
# Constants definition
#

PUT = Verb('PUT')
POST = Verb('POST')

GET = Verb('GET')
DELETE = Verb('DELETE')
