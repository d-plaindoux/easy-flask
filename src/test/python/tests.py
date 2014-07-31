# Copyright (C)2014 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

import unittest
import suites

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(suites.fluent_rest.spec.path_parse.suite())
    suite.addTest(suites.fluent_rest.spec.path_match.suite())
    suite.addTest(suites.fluent_rest.spec.verb.suite())
    suite.addTest(suites.fluent_rest.spec.mime.suite())
    suite.addTest(suites.fluent_rest.inspector.inspection.suite())
    suite.addTest(suites.fluent_rest.bridge.wsgi.suite())
    unittest.TextTestRunner(verbosity=2).run(suite)
