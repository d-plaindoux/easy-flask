import unittest
from easy_flask import rest
from easy_flask.exceptions import OverloadedVerbException


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_have_nothing(self):
        def test():
            pass

        self.assertFalse(rest.hasGET(test))
        self.assertFalse(rest.hasPUT(test))
        self.assertFalse(rest.hasPOST(test))
        self.assertFalse(rest.hasDELETE(test))

    def test_should_have_GET(self):
        @rest.GET
        def test():
            pass

        self.assertTrue(rest.hasGET(test))

    def test_should_have_PUT(self):
        @rest.PUT
        def test():
            pass

        self.assertTrue(rest.hasPUT(test))

    def test_should_have_POST(self):
        @rest.POST
        def test():
            pass

        self.assertTrue(rest.hasPOST(test))

    def test_should_have_DELETE(self):
        @rest.DELETE
        def test():
            pass

        self.assertTrue(rest.hasDELETE(test))

    def test_should_have_a_Verb(self):
        @rest.Verb(u'UPLOAD')
        def test():
            pass

        self.assertTrue(rest.hasVerb(test, u'UPLOAD'))

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
