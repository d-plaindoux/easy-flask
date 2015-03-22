# Copyright (C)2015 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.


class WebException(Exception):
    def __init__(self, status, message=None):
        Exception.__init__(self)
        self.status = status
        self.message = message

    @staticmethod
    def notFound(message=None):
        return WebException(404,
                            "Not found" if message is None else message)

    @staticmethod
    def notAcceptable(message=None):
        return WebException(406,
                            "Not acceptable" if message is None else message)


