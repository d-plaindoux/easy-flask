# Copyright (C)2015 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.


class TypeUndefinedException(Exception):
    def __init__(self, *args, **kwargs):
        super(TypeUndefinedException, self).__init__(*args, **kwargs)


class OverloadedInjectException(Exception):
    def __init__(self, *args, **kwargs):
        super(OverloadedInjectException, self).__init__(*args, **kwargs)


class VariableUndefinedException(Exception):
    def __init__(self, *args, **kwargs):
        super(VariableUndefinedException, self).__init__(*args, **kwargs)


class OverloadedVerbException(Exception):
    def __init__(self, *args, **kwargs):
        super(OverloadedVerbException, self).__init__(*args, **kwargs)


class OverloadedProviderException(Exception):
    def __init__(self, *args, **kwargs):
        super(OverloadedProviderException, self).__init__(*args, **kwargs)


class OverloadedProducerException(Exception):
    def __init__(self, *args, **kwargs):
        super(OverloadedProducerException, self).__init__(*args, **kwargs)


class OverloadedPathException(Exception):
    def __init__(self, *args, **kwargs):
        super(OverloadedPathException, self).__init__(*args, **kwargs)


class NotASuitableDefinitionException(Exception):
    def __init__(self, *args, **kwargs):
        super(NotASuitableDefinitionException, self).__init__(*args, **kwargs)
