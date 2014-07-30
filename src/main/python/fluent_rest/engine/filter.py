from fluent_rest.spec import rest
from fluent_rest.spec.path import Path


class SpecificationFilter:
    """
    A Specification filter is able to select a function using its rest
    specification and a bridged request.
    """

    def __init__(self, specification):
        self.specification = specification

    def filter(self, request):
        """
        Method called when the filter must be performed using a given request.
        If the request respects the specification it returns a set of bound
        variables defined in the path. Otherwise it returns None.
        """
        spec = rest.specs(self.specification)

        if spec.hasGivenVerb(request.verb()) is False:
            return None

        if spec.hasGivenConsumes(request.consumes()) is False:
            return None

        if spec.hasGivenProduces(request.produces()) is False:
            return None

        return Path(spec.getPath()).parse(request.path())


