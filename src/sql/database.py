import logging
import os
import sqlite3
import uuid

from tqdm import tqdm

from sql.errors import TablesNotCreatedError
from sql.query import get_query_create_table, get_query_insert_into_table, get_query_unique_index, \
    get_query_lookup_actor_id
from sql.tabledetails import TABLE_DETAILS_LIST, ACTOR_TABLE_DETAILS, \
    CONVERSATION_TABLE_DETAILS, MESSAGE_TABLE_DETAILS
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
        if os.path.exists(database_location):
            raise FileExistsError("Database file already exists.")
        self.database_location = database_location
        self.archive = archive
        self.connection = sqlite3.connect(database_location)
        self.table_details = None
        self.tables_created = False

    def create_tables(self):
        """Create the tables."""
        for table_details in tqdm(TABLE_DETAILS_LIST, desc="Creating Tables", unit="tables"):
            self._create_table(table_details)
        self.connection.commit()
        self.tables_created = True

    def _create_table(self, table_details):
        """
        Create the supplied table.
        :param table_details: Table details for the table to create.
        """
        logging.info(f"Creating '{table_details['name']}' table...")
        get_query_create_table(table_details).run(self.connection)
        logging.info("Enforcing unique columns...")
        unique_index_query = get_query_unique_index(table_details)
        if unique_index_query:
            unique_index_query.run(self.connection)

    def populate(self, create_tables=False):
        """
        Populate the database using the supplied archive.
        :param create_tables: Create tables automatically before population.
        """
        if not self.tables_created:
            if create_tables:
                self.create_tables()
            else:
                raise TablesNotCreatedError("Tables must be created before population")

        for message_file in tqdm(self.archive.get_message_file_list(), desc="Processing Message Files", unit="files"):
            self._process_message_file(message_file)
        self.connection.commit()

    def _process_message_file(self, message_file):
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
        query = "UNINITIALISED"
        conversation_id = self._generate_id()
        try:
            query = get_query_insert_into_table(CONVERSATION_TABLE_DETAILS,
                                                {
                                                    "Conversation_ID": conversation_id,
                                                    "Conversation_Name": conversation
                                                },
                                                allow_duplicates=True)
            query.run(self.connection)
            return conversation_id
        except sqlite3.OperationalError:
            print("Failed to run query: " + query)

    def _add_actor(self, participant):
        query = "UNINITIALISED"
        actor_id = self._generate_id()
        try:
            query = get_query_insert_into_table(ACTOR_TABLE_DETAILS,
                                                {
                                                    "Actor_ID": actor_id,
                                                    "Actor_Name": participant["name"]
                                                },
                                                allow_duplicates=False)
            query.run(self.connection)
            return actor_id
        except sqlite3.OperationalError:
            print("Failed to run query: " + query)

    def _add_message(self, message, conversation_id):
        if "content" not in message:
            logging.info("Skipping message without content")
            return

        query = "UNINITIALISED"
        message_id = self._generate_id()
        try:
            query = get_query_insert_into_table(MESSAGE_TABLE_DETAILS,
                                                {
                                                    "Message_ID": message_id,
                                                    "Actor_ID": self._lookup_sender_id(message["sender_name"]),
                                                    "Conversation_ID": conversation_id,
                                                    "Timestamp": message["timestamp_ms"],
                                                    "Content": message["content"],
                                                },
                                                allow_duplicates=True)
            query.run(self.connection)
            return message_id
        except sqlite3.OperationalError:
            print("Failed to run query: " + query)

    def _lookup_sender_id(self, sender_name):
        query = "UNINITIALISED"
        try:
            query = get_query_lookup_actor_id(sender_name)
            query_result = query.run(self.connection)
            if len(query_result) == 0:
                return "UNKNOWN_ACTOR"
            return query_result[0][0]
        except sqlite3.OperationalError:
            print("Failed to run query: " + query)

    @staticmethod
    def _generate_id():
        return str(uuid.uuid4())
