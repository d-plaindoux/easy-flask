import unittest
from easy_flask.rest import Rest
from easy_flask.exceptions import OverloadedVerbException


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_have_GET(self):
        rest = Rest()

        @rest.GET()
        def test():
            pass

        self.assertTrue(rest.hasGET())

    def test_should_have_PUT(self):
        rest = Rest()

        @rest.PUT()
        def test():
            pass

        self.assertTrue(rest.hasPUT())

    def test_should_have_POST(self):
        rest = Rest()

        @rest.POST()
        def test():
            pass

        self.assertTrue(rest.hasPOST())

    def test_should_have_DELETE(self):
        rest = Rest()

        @rest.DELETE()
        def test():
            pass

        self.assertTrue(rest.hasDELETE())

    def test_should_have_a_Verb(self):
        rest = Rest()

        @rest.Verb(u'UPLOAD')
        def test():
            pass

        self.assertTrue(rest.hasVerb(u'UPLOAD'))


    def test_should_not_have_GET_and_PUT(self):
        rest = Rest()

        try:
            @rest.GET()
            @rest.PUT()
            def test_function_to_be_rejected():
                pass

            self.fail('Cannot have more than one verb')
        except OverloadedVerbException, _:
            pass


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
