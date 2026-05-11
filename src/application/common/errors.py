class ApplicationError(Exception):
    pass


class ValidationError(ApplicationError):
    pass


class UnauthorizedError(ApplicationError):
    pass


class ForbiddenError(ApplicationError):
    pass


class NotFoundError(ApplicationError):
    pass


class ConflictError(ApplicationError):
    pass
