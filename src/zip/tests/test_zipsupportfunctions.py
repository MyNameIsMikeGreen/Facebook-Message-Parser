import unittest

from zip.archiveinspector import _count_list_similarities


class TestZipSupportFunctions(unittest.TestCase):
    """ Tests the functions that support zip validation."""

    def test_list_checking(self):
        # Equal lists should return the length of the primary list
        primary_list = ["a", "b", "c", "d"]
        proposed_list = ["a", "b", "c", "d"]
        self.assertEqual(_count_list_similarities(primary_list, proposed_list), len(primary_list))

        # A superset proposed list should return the length of the primary list
        primary_list = ["a", "b", "c", "d"]
        proposed_list = ["a", "b", "c", "d", "e"]
        self.assertEqual(_count_list_similarities(primary_list, proposed_list), len(primary_list))

        # A subset proposed list should return the length of the proposed list
        primary_list = ["a", "b", "c", "d"]
        proposed_list = ["a", "b", "c"]
        self.assertEqual(_count_list_similarities(primary_list, proposed_list), len(proposed_list))

        # A proposed list containing a subset should return the number of items the proposed list contains that are
        # present in the primary list.
        primary_list = ["a", "b", "c", "d"]
        proposed_list = ["a", "b", "c", "e"]
        self.assertEqual(_count_list_similarities(primary_list, proposed_list), 3)
