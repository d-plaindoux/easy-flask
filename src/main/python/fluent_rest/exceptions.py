"""
Exceptions raised when some operations may fail
"""


class TypeUndefinedException(Exception):
    def __init__(self, *args, **kwargs):
        super(TypeUndefinedException, self).__init__(*args, **kwargs)


class VariableUndefinedException(Exception):
    def __init__(self, *args, **kwargs):
        super(VariableUndefinedException, self).__init__(*args, **kwargs)


class OverloadedVerbException(Exception):
    def __init__(self, *args, **kwargs):
        super(OverloadedVerbException, self).__init__(*args, **kwargs)


class OverloadedPathException(Exception):
    def __init__(self, *args, **kwargs):
        super(OverloadedPathException, self).__init__(*args, **kwargs)


class NotASuitableDefinitionException(object):
    def __init__(self, *args, **kwargs):
        super(NotASuitableDefinitionException, self).__init__(*args, **kwargs)


