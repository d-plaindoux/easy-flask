import unittest
from easy_rest import rest
from easy_rest.exceptions import OverloadedVerbException


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_have_GET(self):
        @rest.GET
        def test():
            pass

        self.assertTrue(rest.specification(test).hasVerb(u'GET'))

    def test_should_have_PUT(self):
        @rest.PUT
        def test():
            pass

        self.assertTrue(rest.specification(test).hasVerb(u'PUT'))

    def test_should_have_POST(self):
        @rest.POST
        def test():
            pass

        self.assertTrue(rest.specification(test).hasVerb(u'POST'))

    def test_should_have_DELETE(self):
        @rest.DELETE
        def test():
            pass

        self.assertTrue(rest.specification(test).hasVerb(u'DELETE'))

    def test_should_have_a_Verb(self):
        @rest.Verb(u'UPLOAD')
        def test():
            pass

        self.assertTrue(rest.specification(test).hasVerb(u'UPLOAD'))

    def test_should_not_have_GET_and_PUT(self):
        try:
            @rest.GET
            @rest.PUT
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
