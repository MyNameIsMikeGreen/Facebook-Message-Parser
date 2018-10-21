import unittest
from sqlgenerator import SqlGenerator


class TestSql(unittest.TestCase):

    def test_table_creation(self):
        messages_table_details = {
            "name": "Messages",
            "rows": [
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

        actual_query = SqlGenerator.get_query_create_table(messages_table_details)

        self.assertEqual(actual_query, correct_query)
