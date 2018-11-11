import argparse
import os
from zipfile import ZipFile

from zip.zipconstants import EXPECTED_SUBDIRECTORIES, MESSAGES


class ArchiveInspector(object):
    """
    Functions for inspecting Facebook data archive ZIPs.
    """

    @staticmethod
    def check_archive(archive_path, exception=argparse.ArgumentTypeError):
        """
        Type check for archive argument. Intended for use with argparse type checking.
        :param archive_path: Path supplied as value for archive in system arguments.
        :param exception: Exception to be thrown if archive is invalid. argparse.ArgumentTypeError by default.
        :return: archive_path if valid. Raises errors if not valid.
        """
        if not os.path.isfile(archive_path):
            raise exception("There is no file at the supplied archive location.")
        if not ArchiveInspector.file_is_archive(archive_path):
            raise exception("The supplied file does not look like a valid Facebook archive.")
        return archive_path

    @staticmethod
    def file_is_archive(file_path, confidence=0.8):
        """
        Determines whether a file is probably a Facebook archive file based on the subdirectories the archive contains.
        :type file_path: Path of file to check.
        :param confidence: 0 to 1 confidence value representing what percentage of common subdirectories the provided
        zip must have with the set of expected subdirectories in a typical Facebook archive.
        :return: True if the file is of similar format to a Facebook archive file. Else, False.
        """
        if not 0 < confidence <= 1:
            raise ValueError("Confidence value must be: 0 < confidence <= 1")

        # Get list of all items at the root of the archive
        with ZipFile(file_path, "r") as zip_file:
            name_list = zip_file.namelist()
        top_level_names = {name.split("/")[0] for name in name_list}

        # Check that the messages subdirectory is present
        if MESSAGES not in top_level_names:
            return False

        # Check that there are enough of the expected subdirectories present
        common_directory_names = EXPECTED_SUBDIRECTORIES
        expected_subdir_count = _count_list_similarities(common_directory_names, top_level_names)
        confidence_actual = expected_subdir_count / len(common_directory_names)
        if confidence_actual < confidence:
            return False

        # All checks passed
        return True


def _count_list_similarities(primary, proposed):
    """
    Counts the number of items the proposed list has that are present in the primary list.
    :param primary: List holding the values to be checked for.
    :param proposed: List checking for matches in.
    :return: Number of matches in the proposed list.
    """
    matches = 0
    for item in primary:
        if item in proposed:
            matches += 1
    return matches
