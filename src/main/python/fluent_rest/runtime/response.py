# Copyright (C)2014 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

from fluent_rest.spec.rest import Provider


class WebException(Exception):
    def __init__(self, status, message=None):
        Exception.__init__(self)
        self.status = status
        self.message = message

    @staticmethod
    def notFound():
        return WebException(404, "Not found")

    @staticmethod
    def notAcceptable():
        return WebException(406, "Not acceptable")

        # TBC ...


@Provider(WebException)
def webExceptionProvider(bridge, exception):
    return bridge.failure(exception.status, exception.message)


