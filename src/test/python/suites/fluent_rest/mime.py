import unittest
from fluent_rest.rest import *
from fluent_rest.exceptions import OverloadedPathException


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_have_a_consumes(self):
        @Consumes('application/json')
        def test():
            pass

        self.assertTrue(specs(test).hasGivenConsume('application/json'))

    def test_should_have_two_consumes(self):
        @Consumes('application/json')
        @Consumes('application/xml')
        def test():
            pass

        self.assertTrue(specs(test).hasGivenConsume('application/json'))
        self.assertTrue(specs(test).hasGivenConsume('application/xml'))

    def test_should_have_a_produces(self):
        @Produces('application/json')
        def test():
            pass

        self.assertTrue(specs(test).hasGivenProduce('application/json'))

    def test_should_have_two_produces(self):
        @Produces('application/json')
        @Produces('application/xml')
        def test():
            pass

        self.assertTrue(specs(test).hasGivenProduce('application/json'))
        self.assertTrue(specs(test).hasGivenProduce('application/xml'))


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
