class DBIntegrityException(Exception):
    pass


class DBDataException(Exception):
    pass


class DBUserAlreadyExistsException(Exception):
    pass


class DBUserNotFoundException(Exception):
    pass


class DBUserDeletedException(Exception):
    pass


class DBMessageNotFoundException(Exception):
    pass


class DBMessageDeletedException(Exception):
    pass
