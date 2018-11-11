import os
from abc import ABC, abstractmethod
from zipfile import ZipFile

from zip.errors import InvalidArchiveError
from zip.zipconstants import EXPECTED_SUBDIRECTORIES, MESSAGES

TYPE_JSON = "json"
TYPE_HTML = "html"


class FacebookArchive(ABC):
    """ Representation of a generic Facebook data archive ZIP. """

    __slots__ = ["location", "name_list"]

    def __init__(self, location):
        """
        Holds the meta-data related to a Facebook data archive.
        :param location: Location of the archive.
        """

        # Check that the file is a valid archive before importing.
        if not os.path.isfile(location):
            raise FileNotFoundError("No file found at: " + location)
        if not FacebookArchive.file_is_archive(location):
            raise InvalidArchiveError("The supplied archive is invalid.")

        self.location = location

        # Store a list of all items so that it does not need to be re-opened several times.
        with ZipFile(self.location, "r") as zip_file:
            self.name_list = zip_file.namelist()

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
        :return: TODO
        """
        pass

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

    @staticmethod
    def get_archive_type(file_path):
        """
        Determines the type of archive at a path.
        :param file_path: Path to the archive to test.
        :return: Name of one of the Facebook archive types.
        """
        # TODO: Implement a more rigorous check of archive type.
        with ZipFile(file_path, "r") as zip_file:
            name_list = zip_file.namelist()
        if "index.html" in name_list:
            return TYPE_HTML
        else:
            return TYPE_JSON


class FacebookJsonArchive(FacebookArchive):
    """ Representation of a JSON Facebook data archive ZIP. """
    def __init__(self, location):
        super().__init__(location)
        self.type = TYPE_JSON

    def get_message_file_list(self):
        """
        Get the list of all message files in the archive.
        :return: A list of all message file paths.
        """
        return [item for item in self.name_list if os.path.basename(item) == "message.json"]

    def parse_message_file(self, message_file):
        pass


class FacebookHtmlArchive(FacebookArchive):
    """ Representation of a HTML Facebook data archive ZIP. """
    def __init__(self, location):
        super().__init__(location)
        self.type = TYPE_HTML

    def get_message_file_list(self):
        """
        Get the list of all message files in the archive.
        :return: A list of all message file paths.
        """
        return [item for item in self.name_list if os.path.basename(item) == "message.html"]

    def parse_message_file(self, message_file):
        pass


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
