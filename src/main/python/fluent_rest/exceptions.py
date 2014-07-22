"""
Exceptions raised when some operations may fail
"""


class OverloadedVerbException(Exception):
    def __init__(self, *args, **kwargs):
        super(OverloadedVerbException, self).__init__(*args, **kwargs)


class OverloadedPathException(Exception):
    def __init__(self, *args, **kwargs):
        super(OverloadedPathException, self).__init__(*args, **kwargs)


class NotASuitableDefinitionException(object):
    def __init__(self, *args, **kwargs):
        super(NotASuitableDefinitionException, self).__init__(*args, **kwargs)


