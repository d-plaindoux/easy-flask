import unittest
from easy_rest import rest
from easy_rest.exceptions import OverloadedPathException


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_have_a_consumes(self):
        @rest.Consumes('application/json')
        def test():
            pass

        self.assertTrue(
            rest.specification(test).hasConsumes('application/json')
        )

    def test_should_have_a_consumes(self):
        @rest.Consumes('application/json')
        @rest.Consumes('application/xml')
        def test():
            pass

        self.assertTrue(
            rest.specification(test).hasConsumes('application/json')
        )

        self.assertTrue(
            rest.specification(test).hasConsumes('application/xml')
        )


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
