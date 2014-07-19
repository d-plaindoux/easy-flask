import unittest
import suites

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(suites.easy_flask.verb.suite())
    suite.addTest(suites.easy_flask.path.suite())
    unittest.TextTestRunner(verbosity=2).run(suite)
