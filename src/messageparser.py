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


def get_all_table_details():
    """
    Get a list of all table details to be modelled.
    :return: A list of each table details JSON, one for each table.
    """
    messages_table_details = {
        "name": "Messages",
        "columns": [
            {
                "name": "Message_ID",
                "type": "integer",
                "attributes": ["primary", "key", "autoincrement"]
            },
            {
                "name": "Actor_ID",
                "type": "integer"
            },
            {
                "name": "Conversation_ID",
                "type": "integer"
            },
            {
                "name": "Timestamp",
                "type": "integer"
            },
            {
                "name": "Content",
                "type": "text"
            }
        ]
    }

    actor_table_details = {
        "name": "Actors",
        "columns": [
            {
                "name": "Actor_ID",
                "type": "integer",
                "attributes": ["primary", "key", "autoincrement"]
            },
            {
                "name": "Actor_Name",
                "type": "text"
            }
        ]
    }

    conversation_table_details = {
        "name": "Conversations",
        "columns": [
            {
                "name": "Conversation_ID",
                "type": "integer",
                "attributes": ["primary", "key", "autoincrement"]
            },
            {
                "name": "Conversation_Name",
                "type": "text"
            }
        ]
    }

    return [messages_table_details, actor_table_details, conversation_table_details]


if __name__ == '__main__':
    args = parse_arguments()
    archive = import_archive(args.archive)
    database = FacebookArchiveDatabase(archive)
    database.create_tables(get_all_table_details())

