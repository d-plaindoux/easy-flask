"""
TODO
"""


class OverloadedVerbException(Exception):
    def __init__(self, *args, **kwargs):
        super(OverloadedVerbException, self).__init__(*args, **kwargs)


class OverloadedPathException(Exception):
    def __init__(self, *args, **kwargs):
        super(OverloadedPathException, self).__init__(*args, **kwargs)
