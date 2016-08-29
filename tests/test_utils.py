# -*- coding: utf-8 -*-

"""
test_utils
----------------------------------

Tests for `utils` module.
"""

import unittest

from ar_too.utils import normalize_url

class TestNormalizeUrl(unittest.TestCase):
    def test_normalize_url(self):
        self.assertEqual('http://a/b', normalize_url('http://a/b/'))
        self.assertEqual('https://a/b', normalize_url('https://a/b/'))
        self.assertEqual('http://a/b', normalize_url('a/b/'))

if __name__ == '__main__':
    unittest.main()
