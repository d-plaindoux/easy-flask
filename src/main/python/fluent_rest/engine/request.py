"""
TODO
"""


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
        return Request('GET', path, consumes, produces)

    @classmethod
    def post(cls, path, consumes, produces, data):
        return Request('POST', path, consumes, produces, data)

    @classmethod
    def put(cls, path, consumes, produces, data):
        return Request('PUT', path, consumes, produces, data)

    @classmethod
    def delete(cls, path, consumes, produces):
        return Request('DELETE', path, consumes, produces)