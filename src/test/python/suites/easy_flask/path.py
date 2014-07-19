import unittest
from easy_flask.rest import Rest
from easy_flask.exceptions import OverloadedPathException


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_have_a_path(self):
        rest = Rest()

        @rest.Path('a/path')
        def test():
            pass

        self.assertEqual(rest.getPath(), 'a/path')

    def test_should_not_have_Path_twice(self):
        rest = Rest()

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
