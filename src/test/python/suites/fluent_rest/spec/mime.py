import unittest
from fluent_rest.spec.rest import *


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_have_a_consumes(self):
        @Consumes('application/json')
        def test():
            pass

        self.assertTrue(specs(test).hasGivenConsumes('application/json'))

    def test_should_have_two_consumes(self):
        @Consumes('application/json')
        @Consumes('application/xml')
        def test():
            pass

        self.assertTrue(specs(test).hasGivenConsumes('application/json'))
        self.assertTrue(specs(test).hasGivenConsumes('application/xml'))

    def test_should_have_a_produces(self):
        @Produces('application/json')
        def test():
            pass

        self.assertTrue(specs(test).hasGivenProduces('application/json'))

    def test_should_have_two_produces(self):
        @Produces('application/json')
        @Produces('application/xml')
        def test():
            pass

        self.assertTrue(specs(test).hasGivenProduces('application/json'))
        self.assertTrue(specs(test).hasGivenProduces('application/xml'))


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
