# Copyright (C)2016 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

from fluent_rest.runtime.filter import SpecificationFilter
from fluent_rest.spec.inspection import inspector
from fluent_rest.runtime.response import WebException


class WSGIBridge:
    """
    Generic WSGI bridge
    """

    def __init__(self):
        self.__filters = []
        pass

    def request(self, _):
        raise NotImplemented()

    def response(self, _):
        raise NotImplemented()

    def failure(self, status, message=None):
        raise NotImplemented()

    def __applyUsingProvider(self, data, alt=None):
        alternate = alt if alt else lambda e: self.failure(500, str(data))

        for s in self.__filters:
            instance = s.filterProvider(data)
            if instance:
                return instance.execute(data)

        return alternate(data)

    def __applyUsingSpecification(self, wrapper):
        try:
            for s in self.__filters:
                instance = s.filterRequest(wrapper)
                if instance:
                    response = instance.execute(wrapper.data())
                    return self.response(s.filterResponse(wrapper)(response))
        except WebException, e:
            return self.failure(e.status, e.message)

        return self.failure(404, "Not found")

    def trigger(self, request):
        wrapper = self.request(request)
        try:
            return self.__applyUsingProvider(
                self.__applyUsingSpecification(wrapper)
            )
        except Exception, e:
            try:
                return self.__applyUsingProvider(e)
            except WebException, e:
                return self.failure(e.status, e.message)
            except Exception, e2:
                return self.failure(500, str(e2))

    def register(self, service):
        self.__filters.extend(inspector(service).handle(SpecificationFilter))
        return self

    def bind(self, binder):
        binder(self.trigger)
