# Copyright (C)2014 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

import inspect
from fluent_rest.spec import rest
from fluent_rest.spec.path import Path


class SpecificationInstance:
    def __init__(self, specification, variables):
        self.specification = specification
        self.variables = variables

    def execute(self, data):
        parameters = {}

        for name in inspect.getargspec(self.specification)[0]:
            if name == 'self':
                pass
            elif name == 'data':
                parameters['data'] = data
            else:
                parameters[name] = self.variables(name)

        return self.specification(**parameters)


class SpecificationFilter:
    """
    A Specification filter is able to select a function using its rest
    specification and a bridged request.
    """

    def __init__(self, specification):
        self.specification = specification

    def filterProvider(self, response):
        """
        Method called when a response must be managed transparently using
        providers
        """
        spec = rest.specs(self.specification)

        if spec.hasProvider() and isinstance(response, spec.getProvider()):
            return self.specification
        else:
            return None

    def filterSpecification(self, request):
        """
        Method called when the filter must be performed using a given request.
        If the request respects the specification it returns a set of bound
        variables defined in the path. Otherwise it returns None.
        """
        spec = rest.specs(self.specification)

        if spec.hasGivenVerb(request.verb()) is False:
            return None

        if spec.hasGivenConsumes(request.consumes()) is False:
            return None

        if spec.hasGivenProduces(request.produces()) is False:
            return None

        env = Path.parse(spec.getPath()).accept(request.path())

        if env:
            return SpecificationInstance(self.specification, env)
        else:
            return None

    def __str__(self):
        return str(rest.specs(self.specification))
