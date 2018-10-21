class SqlGenerator(object):

    @staticmethod
    def get_query_create_table(table_details):
        """
        Convert JSON specification of a table into an SQL table creation query for that table.
        :param table_details: JSON defining tables in the form:
         {
             "name": "Messages",
                "cols": [
                    {
                        "name": "Message_ID",
                        "type": "integer",
                        "attributes": ["primary", "key", "autoincrement"]
                    }
                ]
        }
        :return: An SQL query to create the table described.
        """
        col_strings = []
        for col in table_details["cols"]:
            col_string = "{0} {1}".format(col["name"], col["type"])
            if "attributes" in col:
                attributes = " ".join([attribute for attribute in col["attributes"]])
                col_string += " " + attributes
            col_strings.append(col_string)
        table_cols_string = ", ".join(col_strings)

        query = "CREATE table {0}({1})".format(table_details["name"], table_cols_string)
        return query

    @staticmethod
    def get_query_insert_into_table(table_details, input_values):
        """
        Insert a set of values for named columns for a table that is defined with the specification.
        :param table_details: JSON defining tables in the form:
         {
             "name": "Messages",
                "cols": [
                    {
                        "name": "Message_ID",
                        "type": "integer",
                        "attributes": ["primary", "key", "autoincrement"]
                    }
                ]
        }
        :param input_values: JSON key-value pairs for column names and values to be put against those columns.
        :return: An SQL query to insert the desired values.
        """
        raise NotImplementedError("This function has not yet been tested and thus should not be used yet.")
        # Get two lists splitting the key-values in the same respective order
        table_cols = []
        values = []
        for k, v in input_values:
            table_cols.append(k)
            values.append(v)

        table_cols_str = ", ".join(table_cols)
        # TODO: Type checking to remove "'" where necessary
        values_str = ", ".join(["'" + str(value) + "'" for value in values])  # Add the quotes

        query = "INSERT into {0}({1} VALUES {2})".format(table_details["name"], table_cols_str, values_str)
        return query
