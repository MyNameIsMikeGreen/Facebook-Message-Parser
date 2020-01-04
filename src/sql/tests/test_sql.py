import unittest

from sql.query import get_query_create_table, get_query_insert_into_table


class TestSql(unittest.TestCase):
    """ Tests the automated generation of SQL queries. """

    def test_table_creation(self):
        """ Tests the automated generation of the table creation SQL query. """

        messages_table_details = {
            "name": "Messages",
            "columns": [
                {
                    "name": "Message_ID",
                    "type": "integer",
                    "attributes": ["primary", "key", "autoincrement"]
                },
                {
                    "name": "Message_Text",
                    "type": "text"
                },
                {
                    "name": "Message_DateTime",
                    "type": "text"
                },
                {
                    "name": "Message_Sender",
                    "type": "text"
                },
                {
                    "name": "Message_Receiver",
                    "type": "text"
                }
            ]
        }

        correct_query = "CREATE table Messages(" \
                        "Message_ID integer primary key autoincrement, " \
                        "Message_Text text, " \
                        "Message_DateTime text, " \
                        "Message_Sender text, " \
                        "Message_Receiver text)"

        actual_query = str(get_query_create_table(messages_table_details))

        self.assertEqual(actual_query, correct_query)

    def test_table_insertion(self):
        """ Tests the automated generation of the table insertion SQL query. """

        messages_table_details = {
            "name": "Messages",
            "columns": [
                {
                    "name": "Message_ID",
                    "type": "integer"
                },
                {
                    "name": "Message_Text",
                    "type": "text"
                },
                {
                    "name": "Message_DateTime",
                    "type": "text"
                },
                {
                    "name": "Message_Sender",
                    "type": "text"
                },
                {
                    "name": "Message_Receiver",
                    "type": "text"
                }
            ]
        }

        insertion_values = {
            "Message_Text": "This is a message.",
            "Message_DateTime": "2018-08-10 15:15:15",
            "Message_Sender": "Mike",
            "Message_Receiver": "Mike again"
        }

        actual_query = str(get_query_insert_into_table(messages_table_details, insertion_values))
        correct_query = "INSERT into Messages (Message_Text, Message_DateTime, Message_Sender, Message_Receiver) " \
                        "VALUES ('This is a message.', '2018-08-10 15:15:15', 'Mike', 'Mike again')"

        self.assertEqual(actual_query, correct_query)
