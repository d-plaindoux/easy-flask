# Copyright (C)2015 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.


class Request:
    def __init__(self, verb, path, consumes, produces, data=None):
        self.__verb = verb
        self.__path = path
        self.__consumes = consumes
        self.__produces = produces
        self.__data = data

    def verb(self):
        return self.__verb

    def consumes(self):
        return self.__consumes

    def produces(self):
        return self.__produces

    def path(self):
        return self.__path

    def data(self):
        return self.__data

    @classmethod
    def get(cls, path, consumes, produces):
        return cls('GET', path, consumes, produces)

    @classmethod
    def post(cls, path, consumes, produces, data):
        return cls('POST', path, consumes, produces, data)

    @classmethod
    def put(cls, path, consumes, produces, data):
        return cls('PUT', path, consumes, produces, data)

    @classmethod
    def delete(cls, path, consumes, produces):
        return cls('DELETE', path, consumes, produces)