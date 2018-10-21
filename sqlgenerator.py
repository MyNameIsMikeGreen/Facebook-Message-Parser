class SqlGenerator(object):

    @staticmethod
    def get_query_create_table(table_details):
        """
        Convert JSON specification of a table into an SQL table creation query for that table.
        :param table_details: JSON defining tables in the form:
         {
             "name": "Messages",
                "rows": [
                    {
                        "name": "Message_ID",
                        "type": "integer",
                        "attributes": ["primary", "key", "autoincrement"]
                    }
                ]
        }
        :return: An SQL query to create the table described.
        """
        row_strings = []
        for row in table_details["rows"]:
            row_string = "{0} {1}".format(row["name"], row["type"])
            if "attributes" in row:
                attributes = " ".join([attribute for attribute in row["attributes"]])
                row_string += " " + attributes
            row_strings.append(row_string)
        table_rows_string = ", ".join(row_strings)

        query = "CREATE table {0}({1})".format(table_details["name"], table_rows_string)
        return query
