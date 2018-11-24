import argparse

from zip.facebookarchive import TYPE_JSON, TYPE_HTML, FacebookJsonArchive, FacebookHtmlArchive, FacebookArchive


def parse_arguments():
    """
    Performs system argument setup.
    :return: System arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", help="Path to the Facebook archive ZIP.")
    return parser.parse_args()


def import_archive(location):
    """
    Given the location of a Facebook archive, creates the appropriate archive object to represent it.
    :param location: Path to ZIP.
    :return: Some subclass of FacebookArchive.
    """
    archive_type = FacebookArchive.get_archive_type(location)
    if archive_type == TYPE_JSON:
        return FacebookJsonArchive(location)
    elif archive_type == TYPE_HTML:
        return FacebookHtmlArchive(location)
    else:
        raise TypeError("Archive of unknown type found")


if __name__ == '__main__':
    args = parse_arguments()
    archive = import_archive(args.archive)
    print(archive.get_message_file_list())
