import logging
import sqlite3
import uuid

from sql.errors import TablesNotCreatedError
from sql.sqlgenerator import get_query_create_table, get_query_insert_into_table, get_query_unique_index
from sql.sqlutils import run_query
from sql.tabledetails import DEFAULT_TABLE_DETAILS_LIST, DEFAULT_ACTOR_TABLE_DETAILS, \
    DEFAULT_CONVERSATION_TABLE_DETAILS, DEFAULT_MESSAGE_TABLE_DETAILS
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
            logging.info(f"Instantiating '{table_details['name']}' table...")
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
            logging.info(f"Populating data from '{message_file}'...")
            conversation = self.archive.parse_message_file(message_file)

            logging.info("Modelling Conversation...")
            conversation_id = self._add_conversation(conversation)

            logging.info("Extracting actors...")
            for participant in conversation["participants"]:
                _ = self._add_actor(participant)

            logging.info("Extracting messages...")
            for message in conversation["messages"]:
                self._add_message(message, conversation_id)

    def _add_conversation(self, conversation):
        """Add a conversation to the database, return the ID of the created conversation."""
        conversation_name = self._sanitise_string(conversation["title"])
        query = "UNINITIALISED"
        conversation_id = self._generate_id()
        try:
            query = get_query_insert_into_table(DEFAULT_CONVERSATION_TABLE_DETAILS,
                                                {
                                                    "Conversation_ID": conversation_id,
                                                    "Conversation_Name": conversation_name
                                                },
                                                allow_duplicates=True)
            run_query(query, self.connection)
            return conversation_id
        except sqlite3.OperationalError:
            print("Failed to run query: " + query)

    def _add_actor(self, participant):
        participant_name = self._sanitise_string(participant["name"])
        query = "UNINITIALISED"
        actor_id = self._generate_id()
        try:
            query = get_query_insert_into_table(DEFAULT_ACTOR_TABLE_DETAILS,
                                                {
                                                    "Actor_ID": actor_id,
                                                    "Actor_Name": participant_name
                                                },
                                                allow_duplicates=False)
            run_query(query, self.connection)
            return actor_id
        except sqlite3.OperationalError:
            print("Failed to run query: " + query)

    def _add_message(self, message, conversation_id):
        if "content" not in message:
            logging.info("Skipping message without content")
            return

        sender_name = message["sender_name"]
        sender_id = self.lookup_sender_id(sender_name)
        content = message["content"]
        timestamp_ms = message["timestamp_ms"]
        query = "UNINITIALISED"
        message_id = self._generate_id()
        try:
            query = get_query_insert_into_table(DEFAULT_MESSAGE_TABLE_DETAILS,
                                                {
                                                    "Message_ID": message_id,
                                                    "Actor_ID": sender_id,
                                                    "Conversation_ID": conversation_id,
                                                    "Timestamp": timestamp_ms,
                                                    "Content": self._sanitise_string(content),
                                                },
                                                allow_duplicates=True)
            run_query(query, self.connection)
            return message_id
        except sqlite3.OperationalError:
            print("Failed to run query: " + query)

    def lookup_sender_id(self, sender_name):
        # TODO: Add to sqlgenerator.py
        query = "UNINITIALISED"
        try:
            query = f"SELECT Actor_ID FROM Actors WHERE Actor_Name='{self._sanitise_string(sender_name)}'"
            query_result = run_query(query, self.connection)
            if len(query_result) == 0:
                return "UNKNOWN_ACTOR"
            return query_result[0][0]
        except sqlite3.OperationalError:
            print("Failed to run query: " + query)

    @staticmethod
    def _sanitise_string(string):
        # TODO: Stronger sanitisation - escape rather than replace.
        return string.replace("'", "")

    @staticmethod
    def _generate_id():
        return str(uuid.uuid4())
