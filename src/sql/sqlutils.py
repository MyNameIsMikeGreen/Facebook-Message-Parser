import logging
import uuid


def run_query(query_string, con):
    """
    Run a query on a SQLite database.
    :param query_string: Query to run.
    :param con: Connection to run query on.
    :return: Result of query.
    """
    query_id = _generate_id()
    logging.debug(f"Running query ({query_id}): '{query_string}'")
    cur = con.cursor()
    cur.execute(query_string)
    logging.debug(f"Query ({query_id}) ran successfully.")
    return cur.fetchall()


def _generate_id():
    return str(uuid.uuid4())[-12:]
