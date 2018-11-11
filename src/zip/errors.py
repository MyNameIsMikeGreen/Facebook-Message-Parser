class InvalidArchiveError(Exception):
    """ Supplied file is not a valid Facebook data archive. """

    def __init__(self, *args, **kwargs):
        super(self, *args, **kwargs)
