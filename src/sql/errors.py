class TablesNotCreatedError(Exception):
    """ The database has not had tables created by the system. """

    def __init__(self, *args, **kwargs):
        super(self, *args, **kwargs)
