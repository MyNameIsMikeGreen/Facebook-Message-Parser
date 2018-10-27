import unittest
from sqlgenerator import SqlGenerator


class TestSql(unittest.TestCase):

    def test_table_creation(self):
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

        actual_query = SqlGenerator.get_query_create_table(messages_table_details)

        self.assertEqual(actual_query, correct_query)


    def test_table_insertion(self):
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

        actual_query = SqlGenerator.get_query_insert_into_table(messages_table_details, insertion_values)
        correct_query = "INSERT into Messages (Message_Text, Message_DateTime, Message_Sender, Message_Receiver) VALUES ('This is a message.', '2018-08-10 15:15:15', 'Mike', 'Mike again')"

        self.assertEqual(actual_query, correct_query)
