import unittest
from easy_flask import rest
from easy_flask.exceptions import OverloadedPathException


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_have_a_path(self):
        @rest.Path('a/path')
        def test():
            pass

        self.assertTrue(rest.hasPath(test))
        self.assertEqual(rest.getPath(test), 'a/path')

    def test_should_not_have_Path_twice(self):
        try:
            @rest.Path("/a/path")
            @rest.Path("/another/path")
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
