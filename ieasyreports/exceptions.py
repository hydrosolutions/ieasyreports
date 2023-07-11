class TemplateNotValidatedException(Exception):
    """
    Raised when a report is attempted to be generated based
    on an un-validated template.
    """


class InvalidTagException(Exception):
    """
    Raised whenever an invalid tag is provided to the report generator.
    """


class MultipleHeaderTagsException(Exception):
    """
    Raised when there multiple header tags are found in a template.
    """


class MissingHeaderTagException(Exception):
    """
    Raised when no header tag is found in a template.
    """


class MissingDataTagException(Exception):
    """
    Raised when no data tags are found in a template.
    """


class InvalidSpecialParameterException(Exception):
    """
    Raised when an invalid value for a special tag is used.
    """
