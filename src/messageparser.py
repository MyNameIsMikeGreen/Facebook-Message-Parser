import argparse


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

