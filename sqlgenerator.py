class SqlGenerator(object):
    """
    Functions for automatically generating SQL query strings.
    """

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
        for col in table_details["columns"]:
            col_string = "{0} {1}".format(col["name"], col["type"])
            if "attributes" in col:
                attributes = " ".join([attribute for attribute in col["attributes"]])
                col_string += " " + attributes
            col_strings.append(col_string)
        table_cols_string = ", ".join(col_strings)

        query = "CREATE table {0}({1})".format(table_details["name"], table_cols_string)
        return query

    @staticmethod
    def get_query_insert_into_table(table_details, input_map):
        """
        Insert a set of values for named columns for a table that is defined with the specification.
        :param table_details: JSON defining tables in the form:
         {
             "name": "Messages",
                "columns": [
                    {
                        "name": "Message_ID",
                        "type": "integer",
                        "attributes": ["primary", "key", "autoincrement"]
                    }
                ]
        }
        :param input_map: JSON key-value pairs for column names and values to be put against those columns.
        :return: An SQL query to insert the desired values.
        :raises ValueError: The input map contains columns that are not in the table description.
        """

        # Get two lists splitting the key-values in the same respective order
        input_table_cols = []
        input_values = []
        for k, v in input_map.items():
            input_table_cols.append(k)
            input_values.append(v)

        # Check that the input values are valid in the table schema
        schema_table_cols = [col["name"] for col in table_details["columns"]]
        if not set(input_table_cols).issubset(set(schema_table_cols)):
            raise ValueError("Attempted to insert into non-existent column.")

        # Form the SQL query
        table_cols_str = ", ".join(input_table_cols)
        # TODO: Type checking to remove "'" where necessary
        values_str = ", ".join(["'" + str(value) + "'" for value in input_values])  # Add the quotes
        query = "INSERT into {0} ({1}) VALUES ({2})".format(table_details["name"], table_cols_str, values_str)
        return query
