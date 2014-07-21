import unittest
from fluent_rest.rest import *
from fluent_rest.exceptions import OverloadedPathException


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_have_a_path(self):
        @Path('a/path')
        def test():
            pass

        self.assertTrue(specs(test).hasPath())
        self.assertEqual(specs(test).getPath(), 'a/path')

    def test_should_not_have_Path_twice(self):
        try:
            @Path("/a/path")
            @Path("/another/path")
            def test_function_to_be_rejected():
                pass

            self.fail('Cannot have more than one verb')
        except OverloadedPathException, _:
            pass


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
