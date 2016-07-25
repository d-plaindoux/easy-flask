# Copyright (C)2016 D. Plaindoux.
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
    def get(status):
        switcher = {
            400: WebException.badRequest,
            401: WebException.unauthorized,
            402: WebException.paymentRequired,
            404: WebException.notFound,
            406: WebException.notAcceptable
        }

        return switcher.get(status, lambda m: WebException(status, m))

    @staticmethod
    def badRequest(message=None):
        return WebException(400,
                            "Bad request" if message is None else message)

    @staticmethod
    def unauthorized(message=None):
        return WebException(401,
                            "Unauthorized" if message is None else message)

    @staticmethod
    def paymentRequired(message=None):
        return WebException(402,
                            "Payment Required" if message is None else message)

    @staticmethod
    def notFound(message=None):
        return WebException(404,
                            "Not found" if message is None else message)

    @staticmethod
    def notAcceptable(message=None):
        return WebException(406,
                            "Not acceptable" if message is None else message)
