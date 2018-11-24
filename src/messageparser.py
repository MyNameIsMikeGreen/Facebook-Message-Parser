import argparse

from sql.database import FacebookArchiveDatabase
from zip.facebookarchive import import_archive


def parse_arguments():
    """
    Performs system argument setup.
    :return: System arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", help="Path to the Facebook archive ZIP.")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    archive = import_archive(args.archive)
    database = FacebookArchiveDatabase(archive)
    database.create_tables(get_all_table_details())
    database.populate()
