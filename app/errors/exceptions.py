class AppBaseException(Exception):
    pass

class InvalidPasswordError(AppBaseException):
    pass

class FileMissingError(AppBaseException):
    pass

class FileSaveError(AppBaseException):
    pass

class DatabaseCommitError(AppBaseException):
    pass
