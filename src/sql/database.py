import logging
import sqlite3

from sql.errors import TablesNotCreatedError
from sql.sqlgenerator import get_query_create_table, get_query_insert_into_table, get_query_unique_index
from sql.sqlutils import run_query
from sql.tabledetails import DEFAULT_TABLE_DETAILS_LIST, DEFAULT_ACTOR_TABLE_DETAILS
from zip.facebookarchive import FacebookArchive


class FacebookArchiveDatabase(object):
    """ Representation of the SQLite database for a Facebook archive. """

    __slots__ = ["database_location", "archive", "connection", "table_details", "tables_created"]

    def __init__(self, archive: FacebookArchive, database_location=":memory:"):
        """
        Create an empty database.
        :param archive: Some FacebookArchive to model in SQLite.
        :param database_location: Path to store database, in memory by default.
        """
        self.database_location = database_location
        self.archive = archive
        self.connection = sqlite3.connect(database_location)
        self.table_details = None  # No details until created
        self.tables_created = False

    def create_tables(self, table_details_list=DEFAULT_TABLE_DETAILS_LIST):
        """
        Given a table details JSON structure, create the tables defined.
        :param table_details_list: List of table details JSON objects.
        """
        # Create the tables
        for table_details in table_details_list:
            logging.info("Instantiating '{0}' table...".format(table_details["name"]))
            # Create the table
            logging.info("Creating tables...")
            table_creation_query = get_query_create_table(table_details)
            run_query(table_creation_query, self.connection)

            # Set any necessary unique indexes
            logging.info("Enforcing unique columns...")
            unique_index_query = get_query_unique_index(table_details)
            if unique_index_query:
                run_query(unique_index_query, self.connection)

        self.tables_created = True

    def populate(self, create_tables=False):
        """
        Populate the database using the supplied archive. Assumes default table details.
        :param create_tables: Create tables using the default table details list automatically before population.
        """

        # TODO: Look into supporting non-default table details

        # Ensure database is ready for data
        if not self.tables_created:
            if create_tables:
                self.create_tables()
            else:
                raise TablesNotCreatedError("Tables must be created before population")

        for message_file in self.archive.get_message_file_list():
            logging.info("Populating data from '{0}'...".format(message_file))
            conversation = self.archive.parse_message_file(message_file)

            # Extract actors
            logging.info("Extracting actors...")
            for participant in conversation["participants"]:
                participant_name = participant["name"].replace("'", "")  # TODO Escape
                query = "UNINITIALISED"
                try:
                    query = get_query_insert_into_table(DEFAULT_ACTOR_TABLE_DETAILS, {"Actor_Name": participant_name},
                                                        allow_duplicates=False)
                    run_query(query, self.connection)
                except sqlite3.OperationalError:
                    print("Failed to run query: " + query)
