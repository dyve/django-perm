class PermException(Exception):
    """
    Something goes wrong within perm
    """
    pass


class PermAppException(PermException):
    """
    Something goes wrong withtin perm, but it it something that might happen because of they way the app works
    """
    pass


class PermQuerySetNotFound(PermAppException):
    """
    The queryset we were looking for was not defined in the app
    """
    pass
