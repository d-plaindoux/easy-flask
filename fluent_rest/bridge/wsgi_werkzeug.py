# Copyright (C)2015 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

from fluent_rest.bridge.wsgi import WSGIBridge
from fluent_rest.runtime.request import Request


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
