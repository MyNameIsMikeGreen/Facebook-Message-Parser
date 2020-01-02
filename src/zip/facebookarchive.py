import json
import os
import re
from abc import ABC, abstractmethod
from zipfile import ZipFile

from zip.archivetype import ArchiveType
from zip.errors import InvalidArchiveError
from zip.zipconstants import EXPECTED_SUBDIRECTORIES, MESSAGES


class FacebookArchive(ABC):
    """ Representation of a generic Facebook data archive ZIP. """

    __slots__ = ["location", "name_list"]

    def __init__(self, location):
        """
        Holds the meta-data related to a Facebook data archive.
        :param location: Location of the archive.
        """
        self.verify_archive_exists(location)
        self.location = location
        self.name_list = self.get_file_names_from_zip(self.location)
        super().__init__()

    @abstractmethod
    def get_message_file_list(self):
        """
        Get the list of all message files in the archive.
        :return: A list of all message file paths.
        """
        pass

    @abstractmethod
    def parse_message_file(self, message_file):
        """
        Parse a message file within the archive.
        :param message_file: Path to message file to parse.
        :return: Message file as dictionary.
        """
        pass

    @staticmethod
    def get_file_names_from_zip(file_path):
        with ZipFile(file_path, "r") as zip_file:
            return zip_file.namelist()

    @staticmethod
    def verify_archive_exists(file_path):
        """
        Verifies whether an archive exists in the supplied location. Raises an error if not.
        :param file_path: Path to archive file.
        :raises FileNotFoundError if file does not exist.
        :raises InvalidArchiveError if the file is not recognised as an archive.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError("No file found at: " + file_path)
        if not FacebookArchive.file_is_archive(file_path):
            raise InvalidArchiveError("The supplied archive is invalid.")

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

        top_level_names = FacebookArchive.get_top_level_names_from_zip(file_path)
        if MESSAGES not in top_level_names:
            return False

        confidence_actual = FacebookArchive.confidence(EXPECTED_SUBDIRECTORIES, top_level_names)
        if confidence_actual < confidence:
            return False

        return True  # All checks passed

    @staticmethod
    def confidence(expected_names, found_names):
        """
        Calculate confidence value for a list of found top level names vs a list of expected top level names.
        :param expected_names: List of top level names expected to be found.
        :param found_names: List of top level names actually found.
        :return: Confidence value between 0 and 1. 1 represents all expected items present in found items list.
        """
        expected_subdir_count = _count_list_similarities(expected_names, found_names)
        return expected_subdir_count / len(expected_names)

    @staticmethod
    def get_top_level_names_from_zip(file_path):
        """
        Extract top level file names inside a zip at supplied location.
        :param file_path: Path to archive.
        :return: List of top level file names inside archive.
        """
        name_list = FacebookArchive.get_file_names_from_zip(file_path)
        return FacebookArchive.top_level_names(name_list)

    @staticmethod
    def top_level_names(name_list):
        """
        Extract top level name from a list of file paths.
        :param name_list: List of file paths.
        :return: Supplied list containing only the top level names.
        """
        return [name.split("/")[0] for name in name_list]

    @staticmethod
    def get_archive_type(file_path):
        """
        Determines the type of archive at a path.
        :param file_path: Path to the archive to test.
        :return: Facebook archive type.
        """
        # TODO: Implement a more rigorous check of archive type.
        with ZipFile(file_path, "r") as zip_file:
            name_list = zip_file.namelist()
        if "index.html" in name_list:
            return ArchiveType.html
        else:
            return ArchiveType.json


class FacebookJsonArchive(FacebookArchive):
    """ Representation of a JSON Facebook data archive ZIP. """
    def __init__(self, location):
        super().__init__(location)
        self.type = ArchiveType.json

    def get_message_file_list(self):
        """
        Get the list of all message files in the archive.
        :return: A list of all message file paths.
        """
        return [item for item in self.name_list if self._is_message_file(item)]

    def parse_message_file(self, message_file):
        """
        Read in the JSON source as a Python dictionary.
        :param message_file: Path to message file to parse.
        :return: Message file as dictionary.
        """
        with ZipFile(self.location, 'r') as archive:
            return json.loads(archive.read(message_file))

    @staticmethod
    def _is_message_file(filename):
        return bool(re.match("message_\d+.json", os.path.basename(filename)))


@DeprecationWarning
class FacebookHtmlArchive(FacebookArchive):
    """ Representation of a HTML Facebook data archive ZIP. """
    def __init__(self, location):
        super().__init__(location)
        self.type = ArchiveType.html
        self.deprecation_warning()

    def get_message_file_list(self):
        self.deprecation_warning()

    def parse_message_file(self, message_file):
        self.deprecation_warning()

    @staticmethod
    def deprecation_warning():
        raise DeprecationWarning("HTML archives are no longer supported.")


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


def import_archive(location):
    """
    Given the location of a Facebook archive, creates the appropriate archive object to represent it.
    :param location: Path to ZIP.
    :return: Some subclass of FacebookArchive.
    """
    archive_type = FacebookArchive.get_archive_type(location)
    if archive_type == ArchiveType.json:
        return FacebookJsonArchive(location)
    elif archive_type == ArchiveType.html:
        raise TypeError("HTML archives are no longer supported. Please supply a JSON archive.")
    else:
        raise TypeError("Archive of unknown type found")
