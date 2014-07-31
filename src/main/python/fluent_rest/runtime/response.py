# Copyright (C)2014 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

from fluent_rest.spec.rest import Provider


class ResponseProvider:
    def __init__(self):
        pass

    def response(self, bridge):
        return bridge.failure(500, None)


@Provider
class WebException(Exception, ResponseProvider):
    def __init__(self, status, message=None):
        Exception.__init__(self)
        self.status = status
        self.message = message

    def response(self, bridge):
        return bridge.failure(self.status, message=self.message)

    @staticmethod
    def notFound():
        return WebException(404, "Not found")

    @staticmethod
    def notAcceptable():
        return WebException(406, "Not acceptable")

    # TBC ...