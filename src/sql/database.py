import sqlite3

from sql.sqlgenerator import get_query_create_table
from sql.sqlutils import run_query


class FacebookArchiveDatabase(object):
    """ Representation of the SQLite database for a Facebook archive. """

    __slots__ = ["database_location", "archive", "connection"]

    def __init__(self, archive, database_location=":memory:"):
        """
        Create an empty database.
        :param archive: Some FacebookArchive to model in SQLite.
        :param database_location: Path to store database, in memory by default.
        """
        self.database_location = database_location
        self.archive = archive
        self.connection = sqlite3.connect(database_location)

    def create_tables(self, table_details_list):
        """
        Given a table details JSON structure, create the tables defined.
        :param table_details_list: List of table details JSON objects.
        """
        for table_details in table_details_list:
            query = get_query_create_table(table_details)
            run_query(query, self.connection)
