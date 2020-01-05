import argparse
import logging

from sql.database import FacebookArchiveDatabase
from sql.query import Query
from zip.facebookarchive import import_archive


def _parse_arguments():
    """
    Performs system argument setup.
    :return: System arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", help="Path to the Facebook archive ZIP.")
    parser.add_argument("--output", help="Path to the database file to create.")
    parser.add_argument("--log", help="Logging detail level.", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    return parser.parse_args()


def _set_logging_level():
    if args.log:
        numeric_level = getattr(logging, args.log.upper(), None)
        logging.basicConfig(level=numeric_level)


if __name__ == '__main__':
    args = _parse_arguments()
    _set_logging_level()

    database = FacebookArchiveDatabase(import_archive(args.archive), database_location=args.output)
    database.create_tables()
    database.populate()
