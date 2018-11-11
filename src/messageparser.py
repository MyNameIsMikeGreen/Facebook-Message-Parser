import argparse
import logging


def run_query(query_string, con):
    """
    Run a query on a SQLite database.
    :param query_string: Query to run.
    :param con: Connection to run query on.
    :return: Result of query.
    """
    logging.info("Running query: '{}'".format(query_string))
    cur = con.cursor()
    cur.execute(query_string)
    logging.info("Query ran successfully.")
    return cur.fetchall()


def parse_arguments():
    """
    Performs system argument setup.
    :return: System arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", help="Path to the Facebook archive.")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

