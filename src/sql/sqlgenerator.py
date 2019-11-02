import logging


def get_query_unique_index(table_details):
    # e.g: create unique index PaymentInformation_name_start on PaymentInformation ( name, start )
    unique_columns = []
    for column_detail in table_details["columns"]:
        if "unique" in column_detail:  # If data not present, assume not unique
            if column_detail["unique"]:  # Explicitly unique
                unique_columns.append(column_detail["name"])
    if unique_columns:
        unique_columns_clause = ", ".join(unique_columns)
        query = f"CREATE UNIQUE INDEX {table_details['name']}_index on {table_details['name']} ({unique_columns_clause})"
        return query
    else:
        return None


def get_query_create_table(table_details):
    """
    Convert JSON specification of a table into an SQL table creation query for that table.
    :param table_details: JSON defining tables in the form:
     {
        "name": "Messages",
        "columns": [
            {
                "name": "Message_ID",
                "type": "integer",
                "attributes": ["primary", "key", "autoincrement"],
            }
        ]
    }
    :return: An SQL query to create the table described.
    """
    col_strings = []
    for col in table_details["columns"]:
        col_string = f"{col['name']} {col['type']}"
        if "attributes" in col:
            attributes = " ".join([attribute for attribute in col["attributes"]])
            col_string += " " + attributes
        col_strings.append(col_string)
    table_cols_string = ", ".join(col_strings)

    query = f"CREATE table {table_details['name']}({table_cols_string})"
    logging.debug(f"Generated table creation SQL query: '{query}'")
    return query


def get_query_insert_into_table(table_details, input_map, allow_duplicates=True):
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
    :param allow_duplicates: Do not add a new row if an equivalent (ignoring key) already exists.
    :return: An SQL query to insert the desired values.
    :raises ValueError: The input map contains columns that are not in the table description.
    """

    # Get two lists splitting the key-values in the same respective order
    input_table_cols = []
    input_values = []
    for k, v in input_map.items():
        # TODO: Escape illegal characters fully
        input_table_cols.append(str(k).replace("'", ""))
        input_values.append(str(v).replace("'", ""))

    # Check that the input values are valid in the table schema
    schema_table_cols = [col["name"] for col in table_details["columns"]]
    if not set(input_table_cols).issubset(set(schema_table_cols)):
        raise ValueError("Attempted to insert into non-existent column.")

    # Form the SQL query
    table_cols_str = ", ".join(input_table_cols)
    # TODO: Type checking to remove "'" where necessary
    values_str = ", ".join(["'" + str(value) + "'" for value in input_values])  # Add the quotes
    if allow_duplicates:
        ignore_statement = " "
    else:
        ignore_statement = " or IGNORE "
    query = f"INSERT{ignore_statement}into {table_details['name']} ({table_cols_str}) VALUES ({values_str})"
    logging.debug(f"Generated table insertion SQL query: '{query}'")
    return query
