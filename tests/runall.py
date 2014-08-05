# Copyright (C)2014 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

import unittest
import path_parse_test
import path_match_test
import verb_test
import provider_test
import mime_test
import inspection_test
import wsgi_test



if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(path_parse_test.suite())
    suite.addTest(path_match_test.suite())
    suite.addTest(verb_test.suite())
    suite.addTest(provider_test.suite())
    suite.addTest(mime_test.suite())
    suite.addTest(inspection_test.suite())
    suite.addTest(wsgi_test.suite())
    unittest.TextTestRunner(verbosity=2).run(suite)
