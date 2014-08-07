# Copyright (C)2014 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.
import inspect

from fluent_rest.runtime.filter import SpecificationFilter
from fluent_rest.runtime.request import Request
from fluent_rest.inspector.inspection import inspector
from fluent_rest.runtime.response import WebException


class WSGIBridge:
    """
    Generic WSGI bridge
    """

    def __init__(self):
        self.__filters = []
        self.__providers = []
        pass

    def request(self, _):
        raise NotImplemented()

    def response(self, _):
        raise NotImplemented()

    def failure(self, status, message=None):
        raise NotImplemented()

    def __applyUsingProvider(self, data):
        for s in self.__filters:
            instance = s.filterProvider(data)
            if instance:
                return instance.execute(data)

        return self.failure(500, str(data))

    def __applyUsingSpecification(self, wrapper):
        try:
            for s in self.__filters:
                instance = s.filterRequest(wrapper)
                if instance:
                    response = instance.execute(wrapper.data())
                    return self.response(response)
        except WebException, e:
            return self.failure(e.status, e.message)

        return self.failure(404, "Not found")

    def trigger(self, request):
        wrapper = self.request(request)
        try:
            return self.__applyUsingSpecification(wrapper)
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

    def unregister(self, _):
        return self

    def bind(self, binder):
        binder(self.trigger)


class Werkzeug(WSGIBridge):
    def __init__(self):
        WSGIBridge.__init__(self)

    def request(self, input):
        return Request(input.method,
                       input.path,
                       input.headers['CONTENT-TYPE'],
                       input.headers['CONTENT-TYPE'], # TODO(didier) ???
                       input.get_data())              # TODO(didier) ???

    def response(self, response):
        from werkzeug import wrappers

        return wrappers.Response(response)

    def failure(self, status, message=None):
        from werkzeug import wrappers

        return wrappers.BaseResponse(status=status, response=message)
