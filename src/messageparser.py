import argparse
import logging

from sql.database import FacebookArchiveDatabase
from sql.sqlutils import run_query
from zip.facebookarchive import import_archive


def parse_arguments():
    """
    Performs system argument setup.
    :return: System arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", help="Path to the Facebook archive ZIP.")
    parser.add_argument("--log", help="Logging detail level.", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    if args.log:
        numeric_level = getattr(logging, args.log.upper(), None)
        logging.basicConfig(level=numeric_level)

    archive = import_archive(args.archive)
    database = FacebookArchiveDatabase(archive)
    database.create_tables()  # Utilise default table detail specification
    database.populate()

    # ==== Sample queries for testing purposes. Remove in time. ====
    print("Table names:")
    table_names_results = run_query("SELECT name FROM sqlite_master WHERE type='table'", database.connection)
    for table_name_result in table_names_results:
        print(table_name_result[0])

    print("Actor names:")
    name_results = run_query("SELECT Actor_Name FROM Actors", database.connection)
    for name_result in name_results:
        print(name_result[0])
