"""
TODO
"""


class Request:
    def __init__(self, verb, path, consumes, produces):
        self.__verb = verb
        self.__path = path
        self.__consumes = consumes
        self.__produces = produces

    def verb(self):
        return self.__verb

    def consumes(self):
        return self.__consumes

    def produces(self):
        return self.__produces

    def path(self):
        return self.__path